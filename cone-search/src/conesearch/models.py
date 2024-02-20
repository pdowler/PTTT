"""Models for cone-search."""

from enum import Enum

from pydantic import BaseModel, Field

__all__ = [
    "ErrorDetail",
    "ErrorLocation",
    "ErrorModel",
    "Verbosity",
]


class ErrorLocation(str, Enum):
    """Possible locations for an error.

    The first element of ``loc`` in `ErrorDetail` should be chosen from one of
    these values.
    """

    BODY = "body"
    HEADER = "header"
    PATH = "path"
    QUERY = "query"


class ErrorDetail(BaseModel):
    """The detail of the error message."""

    loc: list[str] | None = Field(
        None, title="Location", examples=[["area", "field"]]
    )

    msg: str = Field(..., title="Message", examples=["Some error messge"])

    type: str = Field(..., title="Error type", examples=["some_code"])


class ErrorModel(BaseModel):
    """A structured API error message."""

    detail: list[ErrorDetail] = Field(..., title="Error detail")


class Verbosity(Enum):
    """Levels of verbosity in a simple cone search response."""

    MINIMUM = "minimum"
    DEFAULT = "default"
    ALL = "all"
