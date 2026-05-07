"""Collection domain mixin for ZhihuClient."""


class CollectionMixin:
    def get_collection_detail(self, collection_id: str) -> dict:
        url = f"https://api.zhihu.com/collections/{collection_id}"
        return self._get(url)

    def get_collection_contents(
        self,
        collection_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"https://api.zhihu.com/collections/{collection_id}/contents"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_collection_answers(
        self,
        collection_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"https://api.zhihu.com/collections/{collection_id}/answers"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)
