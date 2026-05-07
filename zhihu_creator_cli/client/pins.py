"""Pin domain mixin for ZhihuClient."""


class PinMixin:
    def get_pin_detail(self, pin_id: str) -> dict:
        url = f"https://api.zhihu.com/pins/{pin_id}"
        return self._get(url)
