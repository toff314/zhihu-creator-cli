"""知乎创作助手 CLI.

提供创作中心文章管理、问题推荐、发布文章和回答等功能。

兼容 CLI-Anything Agent-Native 规范，所有数据命令支持 --json 输出。
"""

__version__ = "0.1.0"
__all__ = ["ZhihuClient", "AuthManager", "get_browser_headers"]
