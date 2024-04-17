"""Definition of SQLAlchemy object mapping entity for Announcements."""

from sqlalchemy import Integer, String, Enum, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from datetime import datetime

from ..models.announcement import Announcement, AnnouncementStatus
from ..models.announcement_details import AnnouncementDetails

__authors__ = ["Nicholas Sanaie"]


class AnnouncementEntity(EntityBase):
    """Model schema used for defining the shape of the 'Announcements' table in the CSXL database."""

    # Name for the announcements table in the database
    __tablename__ = "announcement"

    # Properties for announcement columns

    # unique id (primary_key)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # announcement headline
    headline: Mapped[str] = mapped_column(String, nullable=False, default="")
    # announcement synopsis
    syn: Mapped[str] = mapped_column(String, nullable=False, default="")
    # announcement body
    body: Mapped[str] = mapped_column(String, nullable=False, default="")
    # unqiue announcement slug
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    # announcement image
    image_url: Mapped[str] = mapped_column(String)
    # announcement status
    status: Mapped[AnnouncementStatus] = mapped_column(
        Enum(AnnouncementStatus), nullable=False, default=AnnouncementStatus.DRAFT
    )
    # announcement view count
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # announcement share count
    share_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # announcement published date
    published_date: Mapped[str] = mapped_column(String, nullable=True)
    # announcement modified date
    modified_date: Mapped[str] = mapped_column(String, nullable=True)
    # announcement published date
    archived_date: Mapped[str] = mapped_column(String, nullable=True)

    # one to many relationship between authors (single) and announcements (many)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["UserEntity"] = relationship(back_populates="announcements")

    # one to many relationship between organizations (single) and announcements (many)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["OrganizationEntity"] = relationship(
        back_populates="announcements"
    )

    # one to many relationship between comments (many) and announcements (single)
    comments: Mapped[list["AnnouncementCommentEntity"]] = relationship(
        back_populates="announcement", cascade="all,delete"
    )

    @classmethod
    def from_model(cls, model: Announcement) -> Self:
        """
        Class method that converts an `Announcement` model into a `AnnouncementEntity`

        Parameters:
            - model (Announcement): Model to convert into an entity
        Returns:
            AnnouncementEntity: Entity created from model
        """
        return cls(
            id=model.id,
            headline=model.headline,
            syn=model.syn,
            body=model.body,
            author_id=model.author_id,
            slug=model.slug,
            organization_id=model.organization_id,
            image_url=model.image,
            status=model.status,
            view_count=model.view_count,
            share_count=model.share_count,
            published_date=model.published_date,
            modified_date=model.modified_date,
            archived_date=model.archived_date,
        )

    def to_model(self) -> Announcement:
        """
        Converts a `AnnouncementEntity` object into a `Announcement` model object

        Returns:
            Announcement: `Announcement` object from the entity
        """
        return Announcement(
            id=self.id,
            headline=self.headline,
            syn=self.syn,
            body=self.body,
            author_id=self.author_id,
            slug=self.slug,
            organization_id=self.organization_id,
            organization_slug=self.organization.to_model().slug,
            image=self.image_url,
            status=self.status,
            view_count=self.view_count,
            share_count=self.share_count,
            published_date=self.published_date,
            modified_date=self.modified_date,
            archived_date=self.archived_date,
        )

    def to_details_model(self) -> AnnouncementDetails:
        """
        Converts a 'AnnouncementEntity' object into a 'AnnouncementDetails' model object

        Returns:
            AnnouncementDetails: 'AnnouncementDetails' object based on the entity
        """
        return AnnouncementDetails(
            id=self.id,
            headline=self.headline,
            syn=self.syn,
            body=self.body,
            author_id=self.author_id,
            author=self.author.to_public_model(),
            slug=self.slug,
            organization_id=self.organization_id,
            organization_slug=self.organization.to_model().slug,
            organization=self.organization.to_model(),
            comments=[comment.to_model() for comment in self.comments],
            image=self.image_url,
            status=self.status,
            view_count=self.view_count,
            share_count=self.share_count,
            published_date=self.published_date,
            modified_date=self.modified_date,
            archived_date=self.archived_date,
        )
