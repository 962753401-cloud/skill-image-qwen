#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_image.py - 调用千问 Qwen-Image-3.0 生成或编辑图片（三阶段：optimize / prepare / generate）。

V3 核心升级：三段式令牌链条，新增「提示词优化审核环节」代码级门禁。
  - optimize：模型按官方范本完成审核与优化，提交登记（强制含「优化前后对比+改动说明」防敷衍），
              生成令牌A（绑定优化后提示词内容指纹 sha256），落盘记录，绝不调用真实 API。
  - prepare ：代码检查令牌A（无令牌A -> 拒绝，提示「必须先完成审核优化环节」）；通过后向用户
              原样呈现「原始需求 -> 优化后提示词 -> 改动说明」供确认；生成令牌B，销毁令牌A，绝不调 API。
  - generate：代码检查令牌B（无令牌B / 不匹配 / 内容被篡改 -> 拒绝）；通过后执行 API 调用，
              用完即焚销毁令牌B。

令牌接力：optimize ->(令牌A)-> prepare ->(令牌B)-> generate，少一张门票门就不开；
         模型想从原始需求直接跳到生成，会在 prepare 或 generate 被拦下。
令牌是流程副产品：由代码动态生成内容指纹（sha256(提示词)），非写死密码；模型读源码也无法伪造，
         只有老老实实走完该环节才有资格拿到钥匙。
令牌与内容绑定：每次需求不同令牌不同，提交内容与登记/确认版本不一致即拒绝，防「展示一套、生成另一套」。
用完即焚：prepare 消费令牌A即销毁，generate 成功即销毁令牌B，防拿旧令牌跳步重复执行。
令牌范围：指纹只覆盖提示词内容（sha256(提示词)），尺寸/格式等技术参数从登记记录回取，不纳入指纹；
         门禁锁的核心事实是「用户确认了内容」，技术参数灵活处理，避免改个尺寸就要重走全流程。
拒绝信息反向教学：报错文案即流程指南，被拦下后能自我纠正走回正确流程。
防敷衍机制：optimize 登记强制含「优化前后对比+改动说明」，prepare 原样呈现给用户确认；
         想走过场就得现场编造改动理由，敷衍成本上升；用户确认时能看到优化依据，可发现方向跑偏。

支持两种模式：
  - 文生图 (T2I)：仅 --prompt，根据文本描述生成图像
  - 图生图/图像编辑 (I2I)：--prompt + 1~3 张 --image（URL 或本地路径），基于参考图编辑

纯 Python 标准库实现，无需 pip 安装。密钥从环境变量 DASHSCOPE_API_KEY 读取。
默认模型 qwen-image-3.0（标准版）；--model qwen-image-3.0-pro 切换 Pro 版。

提示词类参数支持 @文件 语法：值以 @ 开头时从其后路径读取文件内容（应对超长提示词，规避命令行长度限制）。
"""

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import secrets
import sys
import tempfile
import time
from pathlib import Path
from urllib import error as urlerror
from urllib import request as urlrequest

DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com"
DEFAULT_MODEL = "qwen-image-3.0"
PRO_MODEL = "qwen-image-3.0-pro"
GENERATION_PATH = "/api/v1/services/aigc/multimodal-generation/generation"

MAX_IMAGES = 3  # I2I 支持 1-3 张参考图

# 尺寸校验（API 文档：像素面积 512*512 ~ 2048*2048，宽高比 1:8 ~ 8:1）
_MIN_AREA = 512 * 512
_MAX_AREA = 2048 * 2048
_MIN_RATIO = 1 / 8
_MAX_RATIO = 8

# 计费档位阈值：面积 > 2,250,000 为 2K 档
_AREA_2K_THRESHOLD = 2250000

# 输入价格（元/张，所有版本/档位一致）
_INPUT_PRICE = 0.02
# 输出价格（元/张）：{(版本, 档位): 单价}
_OUTPUT_PRICE = {
    ("standard", "1k"): 0.18,
    ("standard", "2k"): 0.18,
    ("pro", "1k"): 0.25,
    ("pro", "2k"): 0.50,
}

# 本地图片后缀 -> MIME
_EXT_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
}

# 令牌记录目录（系统临时目录下，保证可写）
OPTIMIZE_DIRNAME = "skill_image_qwen_optimize"  # 令牌A（审核优化）记录
PENDING_DIRNAME = "skill_image_qwen_pending"    # 令牌B（确认）记录
RECORD_TTL_SECONDS = 2 * 60 * 60  # 2 小时后自动失效清理

# 防敷衍：改动说明最短长度（字数），逼模型写出有实质的优化依据
MIN_CHANGE_EXPLANATION_LEN = 20


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def ensure_utf8_stdio():
    """Windows 控制台默认可能是 GBK，强制标准输出/错误为 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def need_key():
    key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not key:
        die(
            "错误：未设置环境变量 DASHSCOPE_API_KEY。\n"
            "请先在当前终端设置（按提示输入，密钥不进入命令历史）：\n"
            "  $env:DASHSCOPE_API_KEY = Read-Host -Prompt 'DASHSCOPE_API_KEY'\n"
            "持久设置时请使用系统环境变量界面或 setx，然后重开终端。\n"
            "API Key 获取：https://help.aliyun.com/zh/model-studio/get-api-key\n"
            "切勿将密钥写入技能文件或在聊天中明文粘贴。"
        )
    return key


def resolve_arg(value):
    """值以 @ 开头时从其后路径读取文件内容（应对超长提示词，规避命令行长度限制）；否则原样返回。"""
    if value and value.startswith("@"):
        path = Path(value[1:])
        if not path.is_file():
            die(f"错误：提示词文件不存在：{value[1:]}")
        return path.read_text(encoding="utf-8")
    return value


def normalize_image(value):
    """URL 原样返回；本地路径读取后转为 data URI。"""
    if value.lower().startswith(("http://", "https://")):
        return value
    path = Path(value)
    if not path.is_file():
        die(f"错误：图片文件不存在：{value}")
    mime, _ = mimetypes.guess_type(str(path))
    if not mime or not mime.startswith("image/"):
        mime = _EXT_MIME.get(path.suffix.lower(), "image/png")
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def validate_size(size):
    """校验 --size：格式 宽*高（如 1024*1024），面积与宽高比须在范围内。无效则 die。"""
    s = size.strip()
    parts = s.split("*")
    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        die(f"错误：无效尺寸 '{size}'。请用 宽*高 格式（如 1024*1024），或不指定由模型自动推荐。")
    w, h = int(parts[0]), int(parts[1])
    area = w * h
    if not (_MIN_AREA <= area <= _MAX_AREA):
        die(f"错误：尺寸像素面积须在 {_MIN_AREA}（512*512）~ {_MAX_AREA}（2048*2048），"
            f"当前 {w}*{h}={area}。")
    ratio = w / h
    if not (_MIN_RATIO <= ratio <= _MAX_RATIO):
        die(f"错误：尺寸宽高比须在 1:8 ~ 8:1，当前 {w}*{h}={ratio:.2f}。")


def build_payload(params):
    """构造 API 请求体。I2I 时 content 为 [图片..., 文本]；T2I 时为 [文本]。"""
    content = []
    for img in params.get("images") or []:
        content.append({"image": normalize_image(img)})
    content.append({"text": params["prompt"]})

    parameters = {"prompt_extend": params["prompt_extend"]}
    if params.get("prompt_extend_mode"):
        parameters["prompt_extend_mode"] = params["prompt_extend_mode"]
    if params.get("size"):
        parameters["size"] = params["size"]
    n = params.get("n", 1)
    if n and n != 1:
        parameters["n"] = n
    if params.get("negative_prompt"):
        parameters["negative_prompt"] = params["negative_prompt"]
    if params.get("seed") is not None:
        parameters["seed"] = params["seed"]
    if params.get("watermark"):
        parameters["watermark"] = True

    return {
        "model": params["model"],
        "input": {"messages": [{"role": "user", "content": content}]},
        "parameters": parameters,
    }


def call_api(key, base_url, payload):
    endpoint = base_url.rstrip("/") + GENERATION_PATH
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urlrequest.Request(endpoint, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {key}")
    try:
        with urlrequest.urlopen(req, timeout=300) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urlerror.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        die(f"API 错误 [HTTP {e.code}]：{detail or e.reason}")
    except urlerror.URLError as e:
        die(f"网络错误：{e.reason}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        die(f"错误：响应非 JSON：{raw[:800]}")


def download_url(url, out_path):
    req = urlrequest.Request(url, method="GET")
    try:
        with urlrequest.urlopen(req, timeout=180) as resp:
            data = resp.read()
    except urlerror.URLError as e:
        die(f"下载图片失败：{e.reason}")
    out_path.write_bytes(data)


def calc_cost(usage, model):
    """根据响应 usage 与模型计算费用明细。"""
    if not usage:
        return None
    model_type = "pro" if "pro" in model.lower() else "standard"
    model_label = "Pro 版" if model_type == "pro" else "标准版"
    input_count = usage.get("input_image_count", 0)
    output_count = usage.get("output_image_count", 0)
    out_type = usage.get("output_image_type", "")
    out_tier = "2k" if "2k" in out_type else "1k"
    unit = _OUTPUT_PRICE[(model_type, out_tier)]
    input_cost = input_count * _INPUT_PRICE
    output_cost = output_count * unit
    return {
        "model_label": model_label,
        "out_tier": out_tier,
        "input_count": input_count,
        "output_count": output_count,
        "unit": unit,
        "input": input_cost,
        "output": output_cost,
        "total": input_cost + output_cost,
    }


def save_images(result, params):
    """保存 API 返回的图片并打印用量与费用。"""
    # API 级别错误
    if result.get("code") or result.get("message"):
        die(f"API 返回错误 [{result.get('code', '-')}]：{result.get('message', '-')}")

    output = result.get("output") or {}
    choices = output.get("choices") or []
    if not choices:
        die(f"错误：响应中无生成结果。完整响应：{json.dumps(result, ensure_ascii=False)[:800]}")

    # 收集所有图片 URL（多图时 choices 含多项）
    image_urls = []
    for ch in choices:
        msg = ch.get("message") or {}
        for item in (msg.get("content") or []):
            if item.get("image"):
                image_urls.append(item["image"])
    if not image_urls:
        die(f"错误：响应 choices 中无图片。完整响应：{json.dumps(result, ensure_ascii=False)[:800]}")

    out_path = Path(params["output"]).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    saved = []
    n = len(image_urls)
    for i, url in enumerate(image_urls, 1):
        if n == 1:
            target = out_path
        else:
            target = out_path.with_name(f"{out_path.stem}-{i}{out_path.suffix}")
        download_url(url, target)
        saved.append(target)
        print(f"图片 {i}/{n}：{target}")

    # 用量与费用
    usage = result.get("usage") or {}
    if usage:
        print(f"\n--- 用量 ---")
        print(f"输出尺寸：{usage.get('output_width', '?')}x{usage.get('output_height', '?')}")
        print(f"输入图片数：{usage.get('input_image_count', 0)}（{usage.get('input_image_type', '-')}）")
        print(f"输出图片数：{usage.get('output_image_count', len(saved))}（{usage.get('output_image_type', '-')}）")
        cost = calc_cost(usage, params["model"])
        if cost:
            print(f"\n--- 费用 ---")
            print(f"版本：{cost['model_label']} | 输出档位：{cost['out_tier'].upper()}")
            print(f"输入费用：{cost['input_count']} 张 x {_INPUT_PRICE:.2f} = {cost['input']:.2f} 元")
            print(f"输出费用：{cost['output_count']} 张 x {cost['unit']:.2f} = {cost['output']:.2f} 元")
            print(f"合计费用：{cost['total']:.2f} 元")

    req_id = result.get("request_id")
    if req_id:
        print(f"请求ID：{req_id}")
    print(f"\n已保存 {len(saved)} 张图片")


def default_output():
    ts = time.strftime("%Y%m%d_%H%M%S")
    return f"output/qwen_image_{ts}.png"


def mode_label(images):
    if not images:
        return "文生图 (T2I)"
    return "图生图/图像编辑 (I2I)"


def model_label_of(model):
    return "Pro 版" if "pro" in model.lower() else "标准版"


def check_image_exists(value):
    """prepare/optimize 阶段校验本地图片存在（URL 跳过）。"""
    if value.lower().startswith(("http://", "https://")):
        return
    if not Path(value).is_file():
        die(f"错误：图片文件不存在：{value}")


# ============================================================
# 令牌与记录机制（三段式链条核心：两个目录，分别存令牌A/令牌B记录）
# ============================================================

def _record_base(subdir):
    """令牌记录目录（系统临时目录下，保证可写）。"""
    d = Path(tempfile.gettempdir()) / subdir
    d.mkdir(parents=True, exist_ok=True)
    return d


def optimize_dir():
    """令牌A（审核优化）记录目录。"""
    return _record_base(OPTIMIZE_DIRNAME)


def pending_dir():
    """令牌B（确认）记录目录。"""
    return _record_base(PENDING_DIRNAME)


def compute_fingerprint(prompt):
    """提示词内容指纹 = sha256(prompt)（UTF-8）。令牌与内容绑定，防篡改防复用。"""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def make_token(fingerprint):
    """令牌 = 指纹-随机nonce。nonce 保证同提示词多次登记不互相覆盖。"""
    nonce = secrets.token_hex(4)  # 8 个十六进制字符
    return f"{fingerprint}-{nonce}"


def record_path(token, base_dir):
    """根据令牌计算记录文件路径；令牌只允许十六进制与连字符，防路径穿越。"""
    allowed = set("0123456789abcdef-")
    if not token or any(c not in allowed for c in token):
        return None
    return base_dir / f"{token}.json"


def save_record(token, data, base_dir):
    """落盘令牌记录（自动写入 token 与 created_at）。"""
    rp = record_path(token, base_dir)
    rec = {**data, "token": token, "created_at": time.time()}
    rp.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    return rp


def load_record(token, base_dir):
    rp = record_path(token, base_dir)
    if rp is None or not rp.is_file():
        return None
    try:
        return json.loads(rp.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def destroy_record(token, base_dir):
    """销毁令牌记录（用完即焚）。"""
    rp = record_path(token, base_dir)
    if rp and rp.is_file():
        try:
            rp.unlink()
        except OSError:
            pass


def cleanup_expired():
    """删除超过 RECORD_TTL_SECONDS 的记录（两个目录），防止堆积。"""
    cutoff = time.time() - RECORD_TTL_SECONDS
    for subdir in (OPTIMIZE_DIRNAME, PENDING_DIRNAME):
        d = _record_base(subdir)
        for f in d.glob("*.json"):
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
            except OSError:
                pass


def validate_optimize_homework(original, optimized, explanation):
    """防敷衍校验：优化前后对比 + 改动说明必须齐备且有实质内容。

    令牌链条只保证「环节发生过」，不保证「环节做得好」；此处通过强制字段 + 改动说明最低长度，
    提升敷衍成本。真正的质量把关交给 prepare 阶段用户确认（能看到优化依据）。
    """
    if not original.strip():
        die("错误：--original-prompt（原始需求）不能为空。optimize 环节必须登记原始需求，"
            "以便用户对比确认。")
    if not optimized.strip():
        die("错误：--optimized-prompt（优化后提示词）不能为空。")
    if not explanation.strip():
        die("错误：--change-explanation（改动说明）不能为空。\n"
            "防敷衍要求：必须说明优化了哪些方面、为什么（如：将简短描述扩展为6步范式、"
            "补充光影氛围、指定图中文字字体与位置、强化保真约束等）。")
    if len(explanation.strip()) < MIN_CHANGE_EXPLANATION_LEN:
        die(f"错误：改动说明过于简略（少于 {MIN_CHANGE_EXPLANATION_LEN} 字），请具体说明"
            "优化了哪些方面、为什么。这是防敷衍作业，也是用户确认的依据。")
    if original.strip() == optimized.strip():
        print(f"⚠ 提示：原始需求与优化后提示词完全相同。若确无优化必要，请在改动说明中明确"
              f"说明理由；用户确认环节会复核。", file=sys.stderr)


# ============================================================
# 阶段一：optimize（审核优化提示词、登记对比+改动说明、返回审核令牌A；绝不调 API）
# ============================================================

def cmd_optimize(args):
    # 解析 @文件 语法（应对超长提示词）
    original = resolve_arg(args.original_prompt)
    optimized = resolve_arg(args.optimized_prompt)
    explanation = resolve_arg(args.change_explanation)

    # 防敷衍校验：优化前后对比 + 改动说明
    validate_optimize_homework(original, optimized, explanation)

    # 技术参数校验
    if len(args.image) > MAX_IMAGES:
        die(f"错误：参考图最多 {MAX_IMAGES} 张，当前 {len(args.image)} 张。")
    if args.n < 1 or args.n > 6:
        die("错误：--n 须在 1-6 之间。")
    if args.seed is not None and not (0 <= args.seed <= 2147483647):
        die("错误：--seed 须在 [0, 2147483647]。")
    if args.size:
        validate_size(args.size)
    # agent 模式仅支持文生图
    if args.image and args.prompt_extend_mode == "agent":
        die("错误：prompt_extend_mode=agent 仅支持文生图（T2I），图生图（I2I）请用 direct。")
    for img in args.image:
        check_image_exists(img)

    params = {
        "prompt": optimized,  # 优化后提示词作为最终生成提示词
        "images": list(args.image),
        "size": args.size,
        "n": args.n,
        "negative_prompt": args.negative_prompt,
        "seed": args.seed,
        "watermark": args.watermark,
        "prompt_extend": args.prompt_extend,
        "prompt_extend_mode": args.prompt_extend_mode,
        "model": args.model,
        "output": args.output if args.output is not None else default_output(),
    }

    # 令牌A：绑定优化后提示词内容指纹（不含技术参数，参数从记录回取）
    fingerprint = compute_fingerprint(optimized)
    token_a = make_token(fingerprint)

    cleanup_expired()
    save_record(token_a, {
        "stage": "optimize",
        "fingerprint": fingerprint,
        "original_prompt": original,
        "optimized_prompt": optimized,
        "change_explanation": explanation,
        "params": params,
    }, optimize_dir())

    print("=== 审核优化登记（阶段一 optimize）===")
    print("【原始需求】")
    print(original)
    print("\n【优化后提示词】")
    print(optimized)
    print("\n【改动说明】")
    print(explanation)
    print("\n=== 生成方案 ===")
    print(f"模式：{mode_label(params['images'])} | 模型：{args.model}（{model_label_of(args.model)}） | "
          f"尺寸：{args.size or '自动'} | 数量：{args.n} | 改写：{args.prompt_extend_mode}")
    if args.image:
        print(f"参考图：{len(args.image)} 张")
    if args.negative_prompt:
        print(f"反向提示词：{args.negative_prompt}")
    if args.seed is not None:
        print(f"种子：{args.seed}")
    print("（费用以实际输出档位为准；标准版 0.18 元/张，Pro 版 1K 0.25 / 2K 0.50 元/张）")
    print("\n=== 审核令牌（Token A）===")
    print(token_a)
    print("\n请将以上「原始需求 -> 优化后提示词 -> 改动说明」原样呈现给用户确认；")
    print("用户确认后用此令牌调用 prepare 阶段。")
    # 注意：本函数绝不调用 call_api -- 这是「绝不调 API」的结构保证。


# ============================================================
# 阶段二：prepare（消费令牌A、登记确认、返回确认令牌B、销毁令牌A；绝不调 API）
# ============================================================

def cmd_prepare(args):
    token_a = args.token
    optimized = resolve_arg(args.optimized_prompt)

    # 检查1：审核优化记录（令牌A）是否存在 -- 无令牌A即拒绝（反向教学）
    rec = load_record(token_a, optimize_dir())
    if rec is None:
        die("错误：无审核优化记录或令牌已失效/已使用。\n"
            "必须先完成 optimize（审核优化）环节拿到审核令牌(Token A)，才能进入 prepare 确认环节。\n"
            "正确流程：optimize -> prepare -> generate。")

    # 检查2：令牌是否匹配
    if rec.get("token") != token_a:
        die("错误：审核令牌(Token A)不匹配。")

    # 检查3：提交的优化后提示词与登记版本是否一致（指纹 + 明文双保险，防篡改）
    if (compute_fingerprint(optimized) != rec.get("fingerprint")
            or optimized != rec.get("optimized_prompt")):
        die("错误：提交的优化后提示词与 optimize 登记版本不一致（防「展示一套、生成另一套」）。\n"
            "请用 optimize 登记时的原始优化后提示词调用 prepare，或重新 optimize 后再 prepare。")

    # 三道检查全过 -- 从记录回取参数与防敷衍作业（供确认环节原样呈现）
    params = dict(rec["params"])
    original = rec.get("original_prompt", "")
    explanation = rec.get("change_explanation", "")
    confirmed = optimized  # 确认版本 = 优化后提示词

    # 令牌B：绑定确认版提示词内容指纹（与令牌A同内容同指纹，但 nonce 不同 -> 不同令牌）
    fingerprint_b = compute_fingerprint(confirmed)
    token_b = make_token(fingerprint_b)

    # 先落盘令牌B（确认记录），再销毁令牌A（用完即焚）；
    # 顺序保证：即使落盘B失败，令牌A仍在，可重试 prepare。
    save_record(token_b, {
        "stage": "prepare",
        "fingerprint": fingerprint_b,
        "optimized_prompt": confirmed,
        "original_prompt": original,
        "change_explanation": explanation,
        "params": params,
        "source_token": token_a,
    }, pending_dir())
    destroy_record(token_a, optimize_dir())  # 消费令牌A即销毁，防拿旧令牌跳步重复执行

    print("=== 确认环节（阶段二 prepare，已通过审核令牌校验）===")
    print("【原始需求】")
    print(original)
    print("\n【优化后提示词（确认版本）】")
    print(confirmed)
    print("\n【改动说明】")
    print(explanation)
    print("\n=== 生成方案（从登记记录回取并锁定，不可篡改）===")
    print(f"模式：{mode_label(params.get('images') or [])} | 模型：{params['model']}（{model_label_of(params['model'])}） | "
          f"尺寸：{params.get('size') or '自动'} | 数量：{params.get('n', 1)} | 改写：{params.get('prompt_extend_mode')}")
    if params.get("images"):
        print(f"参考图：{len(params['images'])} 张")
    if params.get("negative_prompt"):
        print(f"反向提示词：{params['negative_prompt']}")
    if params.get("seed") is not None:
        print(f"种子：{params['seed']}")
    print("\n=== 确认令牌（Token B）===")
    print(token_b)
    print("\n审核令牌(Token A)已销毁（用完即焚）。请用此确认令牌(Token B)调用 generate 阶段生成。")
    # 注意：本函数绝不调用 call_api -- 这是「绝不调 API」的结构保证。


# ============================================================
# 阶段三：generate（消费令牌B、三道检查通过后才调 API、成功后销毁令牌B）
# ============================================================

def cmd_generate(args):
    token_b = args.token
    prompt = resolve_arg(args.prompt)

    # 检查1：确认记录（令牌B）是否存在 -- 无令牌B即拒绝（反向教学）
    rec = load_record(token_b, pending_dir())
    if rec is None:
        die("错误：无确认记录或令牌已失效/已使用。\n"
            "必须先完成 prepare（用户确认）环节拿到确认令牌(Token B)，才能进入 generate 生成环节。\n"
            "正确流程：optimize -> prepare -> generate。")

    # 检查2：令牌是否匹配
    if rec.get("token") != token_b:
        die("错误：确认令牌(Token B)不匹配。")

    # 检查3：提交的提示词与确认版本是否一致（指纹 + 明文双保险，防篡改）
    if (compute_fingerprint(prompt) != rec.get("fingerprint")
            or prompt != rec.get("optimized_prompt")):
        die("错误：提交的提示词与 prepare 确认版本不一致（防「展示一套、生成另一套」）。\n"
            "请用 prepare 确认的提示词调用 generate，或重新 optimize -> prepare 后再 generate。")

    # 三道检查全过 -- 从记录回取并锁定参数（-o 可覆盖输出路径）
    params = dict(rec["params"])
    if args.output is not None:
        params["output"] = args.output
    params["prompt"] = prompt  # 用确认版提示词

    # 先回显方案（确认已过三道门，且无 Key 时也能看到将生成什么）
    mlabel = model_label_of(params["model"])
    print(f"模式：{mode_label(params.get('images') or [])} | 模型：{params['model']}（{mlabel}） | "
          f"尺寸：{params.get('size') or '自动'} | 数量：{params.get('n', 1)} | 改写：{params.get('prompt_extend_mode')}")
    if params.get("images"):
        print(f"参考图：{len(params['images'])} 张")

    key = need_key()
    base_url = os.environ.get("DASHSCOPE_BASE_URL", "").strip() or DEFAULT_BASE_URL

    payload = build_payload(params)
    result = call_api(key, base_url, payload)
    save_images(result, params)

    # 成功后立即销毁令牌B（用完即焚），防止复用。
    # 仅此处可达：call_api / save_images 失败会 die 退出，跳过销毁，从而允许同令牌重试。
    destroy_record(token_b, pending_dir())
    print("确认令牌(Token B)已销毁，不可复用。")


# ============================================================
# 入口：子命令派发（无直接生成路径，裸调用直接报错）
# ============================================================

def main():
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(
        description="调用千问 Qwen-Image-3.0 生成或编辑图片（三阶段：optimize 审核优化 / prepare 确认 / generate 生成）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "三阶段令牌链条工作流（代码兜底，生成前必须审核优化+确认提示词）：\n"
            "  1) optimize：按官方范本审核优化提示词，登记「优化前后对比+改动说明」，返回审核令牌(Token A)，绝不调 API。\n"
            "  2) 将「原始需求->优化后提示词->改动说明」回显用户确认。\n"
            "  3) prepare：用令牌A+优化后提示词登记确认（过三道检查），返回确认令牌(Token B)，销毁令牌A，绝不调 API。\n"
            "  4) generate：用令牌B+确认版提示词生成（过三道检查后才调 API），成功后销毁令牌B。\n\n"
            "令牌接力：optimize->(A)->prepare->(B)->generate，少一张门票门就不开。\n"
            "提示词类参数支持 @文件 语法（值以 @ 开头时从其后路径读取文件内容，应对超长提示词）。\n\n"
            "示例：\n"
            "  optimize 文生图：python generate_image.py optimize --original-prompt \"画只猫\" --optimized-prompt \"<优化后>\" --change-explanation \"<改动说明>\"\n"
            "  optimize 图生图：python generate_image.py optimize --original-prompt \"换背景\" --optimized-prompt \"<优化后>\" --change-explanation \"<改动说明>\" --image photo.png\n"
            "  prepare：        python generate_image.py prepare --token <令牌A> --optimized-prompt \"<优化后>\"\n"
            "  generate：       python generate_image.py generate --token <令牌B> --prompt \"<确认版提示词>\"\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ---- optimize ----
    p_opt = sub.add_parser("optimize", help="审核优化提示词、登记对比+改动说明、返回审核令牌A（不调 API）")
    p_opt.add_argument("--original-prompt", required=True, help="原始需求/初始提示词（必需；可用 @文件）")
    p_opt.add_argument("--optimized-prompt", required=True, help="优化后提示词（必需；可用 @文件）")
    p_opt.add_argument("--change-explanation", required=True,
                       help="改动说明：优化了什么、为什么（防敷衍作业；可用 @文件）")
    p_opt.add_argument("--image", action="append", default=[], metavar="URL_OR_PATH",
                       help="参考图 URL 或本地路径（1-3 张，可重复；不传则为文生图）")
    p_opt.add_argument("--size", default=None,
                       help="输出分辨率，格式 宽*高（如 1024*1024）；不指定则模型自动推荐")
    p_opt.add_argument("--n", type=int, default=1, help="输出图片数量（1-6，默认 1）")
    p_opt.add_argument("--negative-prompt", dest="negative_prompt", default=None,
                       help="反向提示词，描述不希望出现的内容")
    p_opt.add_argument("--seed", type=int, default=None,
                       help="随机数种子 [0, 2147483647]，固定种子可稳定结果")
    p_opt.add_argument("--watermark", action="store_true", help="添加水印（默认不添加）")
    p_opt.add_argument("--no-prompt-extend", dest="prompt_extend", action="store_false",
                       help="关闭提示词智能改写（默认开启，建议开启）")
    p_opt.add_argument("--prompt-extend-mode", dest="prompt_extend_mode", default="direct",
                       choices=["direct", "agent"],
                       help="改写方式：direct（默认，T2I/I2I 均支持）/ agent（仅 T2I）")
    p_opt.add_argument("-o", "--output", default=None,
                       help="输出文件路径，默认 output/qwen_image_时间戳.png")
    p_opt.add_argument("--model", default=DEFAULT_MODEL,
                       help=f"模型 id，默认 {DEFAULT_MODEL}（标准版）；Pro 版用 qwen-image-3.0-pro")
    p_opt.set_defaults(func=cmd_optimize)

    # ---- prepare ----
    p_prep = sub.add_parser("prepare", help="用令牌A登记确认、返回确认令牌B（销毁令牌A，不调 API）")
    p_prep.add_argument("--token", required=True, help="optimize 返回的审核令牌(Token A)")
    p_prep.add_argument("--optimized-prompt", required=True,
                        help="与 optimize 登记一致的优化后提示词（可用 @文件）")
    p_prep.set_defaults(func=cmd_prepare)

    # ---- generate ----
    p_gen = sub.add_parser("generate", help="用令牌B+确认版提示词生成（三道检查后才调 API）")
    p_gen.add_argument("--token", required=True, help="prepare 返回的确认令牌(Token B)")
    p_gen.add_argument("--prompt", required=True, help="与 prepare 确认版本完全一致的提示词（可用 @文件）")
    p_gen.add_argument("-o", "--output", default=None, help="覆盖输出路径（可选）")
    p_gen.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
