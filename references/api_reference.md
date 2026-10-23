# Qwen-Image-3.0 API 参考

## 端点

| 地域 | URL |
|------|-----|
| 通用（默认） | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |
| 华北2-北京（业务空间专属） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |
| 新加坡（业务空间专属） | `POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |

- 鉴权：`Authorization: Bearer $DASHSCOPE_API_KEY`
- Content-Type：`application/json`
- 通用域名仍可正常使用；业务空间专属域名性能更优。脚本默认用通用域名，可用环境变量 `DASHSCOPE_BASE_URL` 覆盖。
- 华北2（北京）与新加坡地域 API Key 与地址不可混用。

## 请求体结构

```json
{
  "model": "qwen-image-3.0",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          { "image": "参考图URL或dataURI" },
          { "text": "文本描述或编辑指令" }
        ]
      }
    ]
  },
  "parameters": {
    "prompt_extend": true,
    "prompt_extend_mode": "direct",
    "size": "1024*1024",
    "n": 1,
    "negative_prompt": "...",
    "seed": 12345,
    "watermark": false
  }
}
```

- **content**：`text` 块**有且仅有一个**，不传或传多个会报错。文生图（T2I）只有 `text`；图生图（I2I）为 `[图片..., text]`，图片 1-3 张。
- 图片值可为公网 URL 或 `data:{mime};base64,{base64}` 格式的 data URI（本地图片）。

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| model | string | 是 | `qwen-image-3.0`（标准版）或 `qwen-image-3.0-pro`（Pro 版） |
| input.messages | array | 是 | 消息列表，仅一条 user 消息 |
| input.messages[].content | array | 是 | 内容块：`{image}` 和/或 `{text}` |
| parameters.prompt_extend | boolean | 否 | 提示词智能改写，默认 `true`（建议开启） |
| parameters.prompt_extend_mode | string | 否 | 改写方式，默认 `direct`。`direct`（DPE）T2I/I2I 均支持；`agent`（APE）**仅 T2I**，I2I 传 `agent` 返回 400 |
| parameters.n | integer | 否 | 输出图片数量 1-6，默认 1 |
| parameters.size | string | 否 | 分辨率，格式 `宽*高`（如 `1024*1024`）。像素面积 512*512 ~ 2048*2048，宽高比 1:8 ~ 8:1。不指定则模型自动推荐 |
| parameters.negative_prompt | string | 否 | 反向提示词，描述不希望出现的内容 |
| parameters.seed | integer | 否 | 随机数种子 [0, 2147483647]，固定种子可稳定结果 |
| parameters.watermark | boolean | 否 | 是否添加水印，默认 `false` |

## 响应体

```json
{
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            { "image": "https://dashscope-result-xx.oss-xx.aliyuncs.com/xxx.png?Expires=xxx" }
          ]
        }
      }
    ]
  },
  "usage": {
    "output_height": 1024,
    "output_width": 1024,
    "input_image_count": 0,
    "input_image_type": "qima_input_1k",
    "output_image_count": 1,
    "output_image_type": "qima_output_1k"
  },
  "request_id": "571ae02f-5c9d-436c-83c2-f221e6df0xxx"
}
```

- **生成图片 URL 有效期 24 小时**，须及时下载保存。输出格式为 PNG。
- `n > 1` 时 `choices` 含多项，每项一张图。
- 任务数据（任务状态、图像 URL 等）仅保留 24 小时，超时自动清除。

### usage 字段说明

| 字段 | 说明 |
|------|------|
| output_width / output_height | 最终输出图片宽高（像素） |
| input_image_count | 输入图片数量；T2I 为 0，I2I 按实际数返回 |
| input_image_type | 输入计量档位：面积<=2,250,000 为 `qima_input_1k`，否则 `qima_input_2k` |
| output_image_count | 实际返回输出图片数量 |
| output_image_type | 输出计量档位：面积<=2,250,000 为 `qima_output_1k`，否则 `qima_output_2k` |

> 2,250,000 像素面积约等于 1500*1500。例如 1024*1024=1,048,576（1K 档），2048*2048=4,194,304（2K 档）。

## 错误响应

```json
{
  "request_id": "31f808fd-8eef-9004-xxxxx",
  "code": "InvalidApiKey",
  "message": "Invalid API-key provided."
}
```

请求成功时不返回 `code`/`message` 字段。错误码详见 https://help.aliyun.com/zh/model-studio/error-code

## 文生图（T2I）示例

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
  "model": "qwen-image-3.0",
  "input": {
    "messages": [
      { "role": "user", "content": [ { "text": "画面是一张竖幅户外人像摄影..." } ] }
    ]
  },
  "parameters": { "prompt_extend": true }
}'
```

## 图生图/图像编辑（I2I）示例

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
  "model": "qwen-image-3.0-pro",
  "input": {
    "messages": [
      { "role": "user", "content": [
        { "image": "https://example.com/photo.png" },
        { "text": "帮我生成一张都市风格女性写真，保留图中人物面部特征..." }
      ] }
    ]
  },
  "parameters": { "prompt_extend": true }
}'
```