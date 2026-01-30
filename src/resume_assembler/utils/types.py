from collections.abc import Mapping, Sequence
from typing import TypeAlias, TypedDict

from redis import Redis

number: TypeAlias = int | float

JsonValue: TypeAlias = (
    str | number | bool | None | list["JsonValue"] | dict[str, "JsonValue"]
)

JsonObject: TypeAlias = Mapping[str, JsonValue]


class Content(TypedDict):
    type: str
    text: str


class StructuredContent(TypedDict):
    ok: bool
    message: str


class JsonRpcResult(TypedDict):
    content: Sequence[Content]
    structuredContent: StructuredContent
    isError: bool


CacheClient: TypeAlias = Redis
