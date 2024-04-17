from enum import Enum
from pydantic import BaseModel
from datetime import datetime

from .public_user import PublicUser
from .organization import Organization
from .announcement_comment import Comment
from .announcement import Announcement

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tanner Macpherson", "Tyler Roth"]


class AnnouncementDetails(Announcement):
    """
    Pydantic model to represent the details of an `Announcement`.
    """

    author: PublicUser
    organization: Organization | None = None
    comments: list[Comment] = []
