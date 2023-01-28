import httpx
import orjson


def patch_httpx():
    httpx._models.jsonlib = orjson  # noqa
    httpx._content.json_dumps = lambda content: orjson.dumps(content, default=str).decode("utf8")
