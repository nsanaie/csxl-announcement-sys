from enum import Enum
from pydantic import BaseModel
from datetime import datetime

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tanner Macpherson", "Tyler Roth"]


class AnnouncementStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Announcement(BaseModel):
    """
    Pydantic model to represent an `Announcement`.
    """

    id: int | None = None
    headline: str
    syn: str
    body: str
    author_id: int
    slug: str
    organization_id: int | None = None
    organization_slug: str | None = None
    image: str | None = None
    status: AnnouncementStatus
    view_count: int = 0
    share_count: int = 0
    published_date: str | None = None
    modified_date: str | None = None
    archived_date: str | None = None
