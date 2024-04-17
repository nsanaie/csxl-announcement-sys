"""Definition of SQLAlchemy object mapping entity for Announcement Comments."""

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from datetime import datetime

from ..models.announcement_comment import Comment

__authors__ = ["Nicholas Sanaie"]


class AnnouncementCommentEntity(EntityBase):
    """Model schema used for defining the shape of the 'Announcement Comments' table in the CSXL database."""

    # Name for the announcement comments table in the database
    __tablename__ = "announcement_comment"

    # Properties for comment columns

    # unique primary key (id) for comments
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # comment text
    text: Mapped[str] = mapped_column(String, nullable=False, default="")
    # posted date
    posted_date: Mapped[str] = mapped_column(String, nullable=False)

    # one to many relationship between comments (many) and authors (single)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["UserEntity"] = relationship(back_populates="announcement_comments")

    # one to many relationship between comments (many) and announcements (single)
    announcement_id: Mapped[int] = mapped_column(ForeignKey("announcement.id"))
    announcement: Mapped["AnnouncementEntity"] = relationship(back_populates="comments")

    @classmethod
    def from_model(cls, model: Comment) -> Self:
        """
        Class method that converts an `Comment` model into a `AnnouncementCommentEntity`

        Parameters:
            - model (Comment): Model to convert into an entity
        Returns:
            AnnouncementCommentEntity: Entity created from model
        """
        return cls(
            id=model.id,
            text=model.text,
            posted_date=model.posted_date,
            author_id=model.author_id,
        )

    def to_model(self) -> Comment:
        """
        Converts a `AnnouncementCommentEntity` object into a `Comment` model object

        Returns:
            Comment: `Comment` object from the entity
        """
        return Comment(
            id=self.id,
            text=self.text,
            author_id=self.author_id,
            author=self.author.to_public_model(),
            posted_date=self.posted_date,
        )
