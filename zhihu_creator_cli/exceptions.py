"""Custom exceptions for Zhihu Creator CLI."""


class ZhihuCliError(Exception):
    """Base exception for all CLI errors."""
    pass


class LoginError(ZhihuCliError):
    """Authentication or session error."""
    pass


class DataFetchError(ZhihuCliError):
    """API request or data retrieval error."""
    pass


class PublishError(ZhihuCliError):
    """Content publishing failure."""
    pass
