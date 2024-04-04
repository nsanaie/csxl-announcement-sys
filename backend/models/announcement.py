from enum import Enum
from pydantic import BaseModel, HttpUrl


from .public_user import PublicUser
from .organization import Organization
from .announcement_comment import Comment

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
    author: PublicUser
    slug: str
    organization: Organization | None = None
    image: HttpUrl | None = None
    status: AnnouncementStatus
    view_count: int = 0
    share_count: int = 0
    comments: list[Comment] = []
    published_date: str | None = None
    modified_date: str | None = None
    archieved_date: str | None = None
