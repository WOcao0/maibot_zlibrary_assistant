"""Zlibrary 助手（MaiBot 插件）。

为 MaiBot（麦麦）提供 Z-Library 图书搜索与下载能力，移植自 AstrBot 插件
`astrbot_plugin_zlibrary_assistant`（作者 OMSociety，MIT 协议）。

模块划分：
    plugin.py        入口、配置模型、生命周期、Tool/Command 组件
    zlib_client.py   Z-Library E-API 异步客户端（账号池、额度、SSRF 防护）
    zlib_security.py URL 安全校验（SSRF 纵深防护）
"""

from .plugin import ZLibraryAssistantPlugin, create_plugin

__all__ = ["ZLibraryAssistantPlugin", "create_plugin"]
