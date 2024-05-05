from pydantic import BaseModel
from datetime import datetime

from .public_user import PublicUser

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tanner Macpherson", "Tyler Roth"]


class Comment(BaseModel):
    """
    Pydantic model to represent a comment on an announcement.
    """

    id: int
    text: str
    author_id: int
    author: PublicUser | None = None
    posted_date: datetime | None = None
