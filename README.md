# skill-image-qwen

一个面向 Codex 的图片生成技能，通过阿里云百炼 Qwen-Image-3.0 完成文生图和图生图编辑。
脚本仅使用 Python 标准库，不依赖第三方包。

## 功能

- 文生图（T2I）与 1-3 张参考图的图生图/图像编辑（I2I）
- 标准版 `qwen-image-3.0` 与 Pro 版 `qwen-image-3.0-pro`
- `optimize -> prepare -> generate` 三段式令牌门禁
- 提示词优化前后对比、改动说明和用户确认记录
- 输出尺寸、用量、费用和请求 ID 汇总
- 本地记录 2 小时后自动失效

## 环境要求

- Python 3.8 或更高版本
- 阿里云百炼 API Key

## 配置密钥

密钥只从进程环境变量 `DASHSCOPE_API_KEY` 读取，不写入源码、配置文件或 Git 仓库。

```powershell
$env:DASHSCOPE_API_KEY = Read-Host -Prompt 'DASHSCOPE_API_KEY'
```

持久配置请使用系统环境变量界面，或使用 `setx` 后重开终端。仓库中的
[.env.example](.env.example) 仅说明变量名且保持为空，脚本不会自动加载 `.env`。

不要在命令行参数、README、Issue、日志或截图中暴露真实密钥。若密钥曾进入
Git 历史，应立即在阿里云百炼控制台吊销并重新生成。

## 三阶段工作流

```powershell
python scripts/generate_image.py optimize --original-prompt "原始需求" --optimized-prompt "优化后提示词" --change-explanation "具体改动与原因"
python scripts/generate_image.py prepare --token "<Token A>" --optimized-prompt "优化后提示词"
python scripts/generate_image.py generate --token "<Token B>" --prompt "优化后提示词"
```

`optimize` 和 `prepare` 不调用付费接口。`generate` 只在令牌检查通过并检测到
`DASHSCOPE_API_KEY` 后请求 API。

提示词参数支持 `@文件` 语法，用于传入超长提示词：

```powershell
python scripts/generate_image.py optimize --original-prompt @original.txt --optimized-prompt @optimized.txt --change-explanation @changes.txt
```

查看完整参数：

```powershell
python scripts/generate_image.py --help
```

## 交给 Codex 的安装提示词

```text
请打开并分析这个技能仓库，确认它是符合 Codex 规范的技能后，下载并安装到 Codex 技能目录；
如果已经安装，则更新到仓库最新内容。安装完成后检查目录结构、SKILL.md frontmatter、脚本语法，
并运行本地三阶段门禁测试，不要调用真实付费生图接口。不要在回复、日志或文件中显示任何账号、
密钥或密码。最后报告安装路径、检查结果、可用状态和未执行项。
技能地址：当前 skill-image-qwen 仓库地址
```

## 测试

测试只使用本地临时目录和模拟令牌，不访问网络，也不调用付费 API：

```powershell
python -m unittest discover -s tests -v
```

## 目录结构

```text
.
├── SKILL.md
├── README.md
├── SECURITY.md
├── agents/openai.yaml
├── references/
├── scripts/generate_image.py
└── tests/test_generate_image.py
```

## License

[MIT](LICENSE)
