from enum import Enum
from pydantic import BaseModel
from datetime import datetime

from .organization import Organization
from .announcement_comment import Comment
from .announcement import Announcement

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tanner Macpherson", "Tyler Roth"]


class AnnouncementDetails(Announcement):
    """
    Pydantic model to represent the details of an `Announcement`.
    """

    organization: Organization | None = None
    comments: list[Comment] = []


class UpvoteBoolean(BaseModel):
    upvoted: bool
