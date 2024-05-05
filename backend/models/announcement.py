from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from .public_user import PublicUser

from backend.models.organization import Organization

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
    author: PublicUser | None = None
    slug: str
    organization_id: int | None = None
    organization_slug: str | None = None
    image: str | None = None
    status: AnnouncementStatus
    published_date: datetime | None = None
    modified_date: datetime | None = None
    archived_date: datetime | None = None
    view_count: int = 0
    share_count: int = 0
    upvote_count: int = 0
