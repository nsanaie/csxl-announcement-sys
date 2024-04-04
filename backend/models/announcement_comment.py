from pydantic import BaseModel

from .public_user import PublicUser

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tanner Macpherson", "Tyler Roth"]


class Comment(BaseModel):
    """
    Pydantic model to represent a comment on an announcement.
    """

    id: int
    text: str
    author: PublicUser
    posted_date: str
