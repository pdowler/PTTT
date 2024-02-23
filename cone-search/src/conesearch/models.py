"""Models for cone-search."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)

__all__ = [
    "ConeSearchParameters",
    "ErrorDetail",
    "ErrorLocation",
    "ErrorModel",
    "ExecutionPhase",
    "Job",
    "JobCreate",
    "JobDescription",
    "JobError",
    "JobResult",
    "JobUpdate",
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


class ConeSearchParameters(BaseModel):
    """Parameters for a Simple Cone Search."""

    ra: Annotated[
        float,
        Field(
            title="Right-ascension",
            description=(
                "A right-ascension in the ICRS coordinate system for the"
                " positon of the center of the cone to search, given in"
                " decimal degrees"
            ),
            examples=[179.5],
        )
    ]

    dec: Annotated[
        float,
        Field(
            title="Declination",
            description=(
                "A declination in the ICRS coordinate system for the positon"
                " of the center of the cone to search, given in decimal"
                " degrees"
            ),
            examples=[59.98],
        )
    ]

    sr: Annotated[
        float,
        Field(
            title="Search radius",
            description=(
                "The radius of the cone to search, given in decimal degrees"
            ),
            examples=[0.5],
        )
    ]

    verb: Annotated[
        Verbosity,
        Field(
            title="Verbosity",
            description=(
                "Choose from `minimum` (minimum columns required to describe"
                " the object), `all` (all available columns), or `default`"
                " (a useful intermediate number of columns)"
            ),
            examples=[Verbosity.ALL],
        )
    ] = Verbosity.DEFAULT


class ExecutionPhase(Enum):
    """Possible execution phases for a UWS job."""

    PENDING = "pending"
    """Accepted by the service but not yet sent for execution."""

    QUEUED = "queued"
    """Sent for execution but not yet started."""

    EXECUTING = "executing"
    """Currently in progress."""

    COMPLETED = "completed"
    """Completed and the results are available for retrieval."""

    ERROR = "error"
    """Failed and reported an error."""

    ABORTED = "aborted"
    """Aborted before it completed."""

    UNKNOWN = "unknown"
    """In an unknown state."""

    HELD = "held"
    """Similar to PENDING, held and not sent for execution."""

    SUSPENDED = "suspended"
    """Execution has started, is currently suspended, and will be resumed."""

    ARCHIVED = "archived"
    """Execution completed some time ago and the results have been deleted."""


class JobError(BaseModel):
    """Failure information about a job."""

    error_code: Annotated[
        str, Field(title="Code for the error", examples=["permission_denied"])
    ]

    message: Annotated[
        str, Field(title="Brief error message", examples=["Permission denied"])
    ]

    detail: Annotated[
        str | None,
        Field(
            title="Extended error message",
            examples=["No access to backend service"],
        )
    ]


class JobResult(BaseModel):
    """A single result from a job."""

    result_id: Annotated[
        str, Field(title="Identifier for the result", examples=["cutout"])
    ]

    url: Annotated[
        str,
        Field(
            title="URL for the result",
            description=(
                "User-facing URL that can be retrieved directly by the user."
                " This may be a signed URL or similar temporary-use URL that"
                " is different from a persistent internal URL."
            ),
            examples=["https://example.com/results/bdfeb7b575c50bb5"],
        )
    ]

    size: Annotated[
        int | None,
        Field(title="Size of the result in bytes", examples=[517135])
    ]

    mime_type: Annotated[
        str | None,
        Field(title="MIME type of the result", examples=["application/fits"])
    ]


class JobDescription(BaseModel):
    """Brief job description used for the job list."""

    job_id: Annotated[str, Field(title="Unique identifier", examples=["1478"])]

    owner: Annotated[
        str, Field(title="Identity of job owner", examples=["rra"])
    ]

    phase: Annotated[
        ExecutionPhase,
        Field(
            title="Current execution phase",
            examples=[ExecutionPhase.EXECUTING],
        )
    ]

    run_id: Annotated[
        str | None,
        Field(
            title="Opaque string provided by client",
            description=(
                "This field is intended for the client to add a unique"
                " identifier to all jobs that are part of a single operation"
                " from the perspective of the client. This may aid in tracing"
                " issues through a complex system, or identifying which"
                " operation a job is part of."
            ),
            examples=["processing-run-40"],
        )
    ]

    creation_time: Annotated[
        datetime,
        Field(
            title="When the job was created", examples=["2023-01-13T14:53:00Z"]
        )
    ]


class Job(JobDescription, Generic[T]):
    """Represents a single UWS job."""

    start_time: Annotated[
        datetime | None,
        Field(
            title="When the job started executing",
            examples=["2024-02-22T14:55:12Z"],
        )
    ]

    end_time: Annotated[
        datetime | None,
        Field(
            title="When the job stopped executing",
            examples=["2024-02-22T15:34:14Z"],
        )
    ]

    destruction_time: Annotated[
        datetime | None,
        Field(
            title="Time at which job should be destroyed",
            description=(
                "At this time, the job will be aborted if it is still running,"
                " its results will be deleted, and all record of the job will"
                " be discarded."
            ),
            examples=["2024-03-22T14:53:00Z"],
        )
    ]

    execution_duration: Annotated[
        timedelta | None,
        Field(
            title="Allowed maximum execution duration",
            description=(
                "Specified in elapsed wall clock time. If not present, there"
                " is no limit. If the job runs for longer than this time"
                " period, it will be aborted."
            ),
            examples=[timedelta(hours=10)],
        )
    ]

    quote: Annotated[
        datetime | None,
        Field(
            title="Expected completion time if started now",
            description=(
                "If not given, the expected duration of the job is not known."
                " If later than the destruction time, the job is not possible"
                " due to resource constraints."
            ),
            examples=["2023-02-13T14:53:00Z"],
        )
    ]

    error: Annotated[JobError | None, Field(title="Error information")]

    parameters: Annotated[T, Field(title="Parameters of the job")]

    results: Annotated[
        list[JobResult] | None, Field(title="Results of the job")
    ]


class JobCreate(BaseModel, Generic[T]):
    """Information required to create a new job."""

    parameters: Annotated[T, Field(title="Parameters of the job")]

    start: Annotated[
        bool, Field(title="Whether to automatically start the job")
    ] = True

    run_id: Annotated[
        str | None,
        Field(
            title="Opaque string provided by client",
            description=(
                "This field is intended for the client to add a unique"
                " identifier to all jobs that are part of a single operation"
                " from the perspective of the client. This may aid in tracing"
                " issues through a complex system, or identifying which"
                " operation a job is part of."
            ),
            examples=["processing-run-40"],
        )
    ]


class JobStart(BaseModel):
    """Body for route to start a job."""

    start: Annotated[Literal[True], Field(title="Must be true")]


class JobUpdate(BaseModel):
    """Requested update to a job.

    Only these fields of a job can be changed after job creation.
    """

    destruction_time: Annotated[
        datetime | None,
        Field(
            title="Time at which job should be destroyed",
            description=(
                "At this time, the job will be aborted if it is still running,"
                " its results will be deleted, and all record of the job will"
                " be discarded."
            ),
            examples=["2024-03-22T14:53:00Z"],
        )
    ]

    execution_duration: Annotated[
        timedelta | None,
        Field(
            title="Allowed maximum execution duration",
            description=(
                "Specified in elapsed wall clock time. If not present, there"
                " is no limit. If the job runs for longer than this time"
                " period, it will be aborted."
            ),
            examples=[timedelta(hours=10)],
        )
    ]
