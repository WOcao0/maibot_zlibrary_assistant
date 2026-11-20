# Zlibrary 助手（MaiBot 插件）

为 [MaiBot（麦麦）](https://docs.maibot.chat) 提供 Z-Library 图书搜索与下载能力，移植自 AstrBot 插件
[`astrbot_plugin_zlibrary_assistant`](https://github.com/OMSociety/astrbot_plugin_zlibrary_assistant)（作者 OMSociety，MIT 协议）。

特性：

- **账号池**：多账号轮换，下载时自动挑选今日剩余额度最多的账号
- **HTML 封面卡片**：搜索结果渲染成带封面/标题/作者/格式的图片直接发到聊天
- **额度管控**：单文件体积上限、每日下载次数、搜索结果条数均可配
- **SSRF 纵深防护**：封面/下载直链请求前做 IP 黑名单 + DNS rebinding 校验（`zlib_security.py`）
- **3 个 LLM 工具 + 2 个命令**，开箱即可被模型自动调用或手动触发

## 安装

1. 把本目录 `omsociety_zlibrary_assistant`（或改名后的插件目录）整体放进 MaiBot 的 `plugins/` 目录：

   ```
   plugins/
   └── omsociety_zlibrary_assistant/
       ├── _manifest.json
       ├── __init__.py
       ├── plugin.py
       ├── zlib_client.py
       ├── zlib_security.py
       └── requirements.txt
   ```

2. 依赖已在 manifest 的 `dependencies` 中声明（`aiohttp` / `aiohttp-socks` / `aiofiles` / `Pillow`），
   MaiBot 加载插件时会自动安装；若自动安装失败，可手动进入 MaiBot 的 Python 环境执行：

   ```bash
   pip install aiohttp aiohttp-socks aiofiles Pillow
   ```

3. 重启 MaiBot（或从 WebUI 重新加载插件），首次加载会自动生成 `config.toml`。

## 配置

在 WebUI「插件配置」页填写，或直接编辑插件目录下的 `config.toml`：

```toml
[plugin]
enabled = true
config_version = "1.0.0"

[zlib]
domain = "z-library.sk"
proxy = ""
max_download_mb = 80
search_limit = 5

[[zlib.accounts]]
name = "account1"
email = ""            # 方式一：邮箱 + 密码
password = ""
remix_userid = ""     # 方式二（推荐）：浏览器登录 z-library 后复制 Cookie 值
remix_userkey = ""
```

账号说明：

- **方式一（邮箱 + 密码）**：走 `/eapi/user/login`，易被 Z-Library 对共享 IP 风控（`#ipd3`）
- **方式二（remix_userid + remix_userkey，推荐）**：浏览器登录 z-library.sk 后按 F12 → 应用/Application → Cookie，
  复制 `remix_userid` / `remix_userkey` 值。走 GET profile 验证，几乎不受 login 风控影响
- 两种方式都填时 remix 优先；可添加多个账号共享每日额度（每个账号每日约 10 次）

其他项：

- `domain`：Z-Library E-API 域名/地址，可填 `z-library.sk`、`https://…`，或 `.onion`（onion 需同时配 SOCKS 代理）
- `proxy`：HTTP/SOCKS 代理；onion 必须填 `socks5://…`
- `max_download_mb`：单文件体积上限（1–512 MiB）
- `search_limit`：搜索默认返回条数（1–8）

## 命令

| 命令 | 作用 |
| --- | --- |
| `/搜书 <关键词>` | 搜索图书，发送封面卡片 + 带编号的文本列表 |
| `/额度` | 查询账号池登录状态与今日剩余下载额度 |

LLM 工具（模型可在对话中自动判断调用）：

- `zlib_search_books`：按关键词搜索（可加 `limit` / `language` / `extension` 过滤）
- `zlib_download_book`：按搜索结果 id 下载（需先在搜索里拿到 id）
- `zlib_get_status`：查询账号池状态与额度

## 故障排查

- **一直提示限流 / 登录失败**：改用 remix 方式登录（见「配置」），或更换代理节点
- **搜索成功但封面空白**：封面 CDN 偶发 513，插件会自动降级为渐变占位，不影响搜索与下载
- **卡片图不出现（只有文字）**：可能是 MaiBot 的 HTML 渲染服务（`render.html2png`）不可用，插件会自动降级为纯文本列表，功能不受影响
- **下载后没有文件发到聊天**：聊天「文件服务」不可用时，插件会把文件保存到
  `data/plugins/com.omsociety.zlibrary-assistant/books/` 并在消息里给出本地路径，可自行取用
- **提示「未配置账号」**：搜索部分域名允许匿名，但下载必须配至少一个账号

## 致谢

原插件：[OMSociety/astrbot_plugin_zlibrary_assistant](https://github.com/OMSociety/astrbot_plugin_zlibrary_assistant)（MIT）
