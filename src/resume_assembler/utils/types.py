from collections.abc import Mapping, Sequence
from typing import TypeAlias

number: TypeAlias = int | float


JSONString: TypeAlias = str
JSONNumber: TypeAlias = float | int
JSONBoolean: TypeAlias = bool
JSONNull: TypeAlias = None
JSONArray: TypeAlias = Sequence
JSONObject: TypeAlias = Mapping
