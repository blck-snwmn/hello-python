from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated, Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints, model_validator

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


class ReadingStatus(StrEnum):
    UNREAD = "unread"
    FINISHED = "finished"


class ReadingItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: UUID = Field(default_factory=uuid4)
    title: Title
    url: HttpUrl | None = None
    status: ReadingStatus = ReadingStatus.UNREAD
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None

    @model_validator(mode="after")
    def finished_state_is_consistent(self) -> Self:
        is_finished = self.status is ReadingStatus.FINISHED
        if is_finished != (self.finished_at is not None):
            raise ValueError("status and finished_at must describe the same state")
        return self

    def finish(self, *, at: datetime | None = None) -> Self:
        finished_at = at or datetime.now(UTC)
        return type(self)(
            id=self.id,
            title=self.title,
            url=self.url,
            status=ReadingStatus.FINISHED,
            created_at=self.created_at,
            finished_at=finished_at,
        )
