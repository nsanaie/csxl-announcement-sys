"""
This Announcements Service is for use with the API to create, edit and delete announcement data in the database.
"""

from fastapi import Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import db_session
from ..models.announcement import Announcement, AnnouncementStatus
from ..models.announcement_comment import Comment
from ..models.announcement_details import AnnouncementDetails
from ..entities.announcement_entity import AnnouncementEntity
from ..entities.announcements_comment_entity import AnnouncementCommentEntity
from ..entities.organization_entity import OrganizationEntity
from ..entities.user_entity import UserEntity
from ..models import User
from .permission import PermissionService

from .exceptions import ResourceNotFoundException

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tyler Roth", "Tanner Macpherson"]


class AnnouncementService:
    """Service for performing CRUD actions on the 'Announcement' table in the database."""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        self._session = session
        self._permission = permission

    def all_published(self) -> list[Announcement]:
        """
        Retrieves all published announcements from the table

        Returns:
            list[Announcement]: List of all published `Announcement`
        """

        entities = (
            self._session.query(AnnouncementEntity)
            .where(AnnouncementEntity.status == AnnouncementStatus.PUBLISHED)
            .order_by(desc(AnnouncementEntity.id))
            .all()
        )
        return [entity.to_model() for entity in entities]

    def get_by_slug(self, slug: str) -> AnnouncementDetails:
        """
        Get the announcement details from a slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique announcement slug

        Returns:
            AnnoucementDetails: Object with corresponding slug

        Raises:
            ResourceNotFoundException if no announcement is found with the corresponding slug
        """
        announcement = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )

        if announcement is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        if announcement.status != AnnouncementStatus.PUBLISHED:
            raise ResourceNotFoundException(
                "Announcement exists, but you do not have permission to view it."
            )

        return announcement.to_details_model()

    def create(self, subject: User, announcement: Announcement) -> Announcement:
        """
        Creates an announcement based on the input object and adds it to the table.
        If the slug is unique in the table, we add a new entry. If not, we raise an exception.

        Parameters:
            subject: a valid User model representing the currently logged in User
            announcement (Announcement): Announcement to add in table.

        Returns:
            Announcement: The object added to the table
        """
        # check user perms
        self._permission.enforce(subject, "announcement.create", f"announcement")

        announcement.id = None

        if (
            not self._session.query(UserEntity)
            .filter_by(id=announcement.author_id)
            .first()
        ):
            raise ResourceNotFoundException(
                "Author user does not exist in the database."
            )
        if (
            not self._session.query(OrganizationEntity)
            .filter_by(id=announcement.organization_id)
            .first()
        ):
            raise ResourceNotFoundException(
                "Organization does not exist in the database."
            )
        if (
            self._session.query(AnnouncementEntity)
            .filter_by(slug=announcement.slug)
            .first()
        ):
            raise ResourceNotFoundException(
                "An announcement with this slug already exists."
            )

        announcement_entity = AnnouncementEntity.from_model(announcement)
        self._session.add(announcement_entity)
        self._session.commit()

        return announcement_entity.to_model()

    def create_comment(self, subject: User, slug: str, comment: Comment) -> Comment:
        """
        Creates an announcement comment based on the input object and adds it to the table.
        If the ID is unique in the table, we add a new entry. If not, we raise an exception.

        Parameters:
            subject: a valid User model representing the currently logged in User
            slug: a unique string representing a unique announcement

        Returns:
            Comment: The object created in the table
        """

        comment.id = None

        announcement = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )

        if announcement is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        author = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == subject.id)
            .one_or_none()
        )

        if author is None:
            raise ResourceNotFoundException("User does not exist in the database.")

        comment_entity = AnnouncementCommentEntity.from_model(comment)
        announcement.comments.append(comment_entity)
        self._session.commit()

        return comment_entity.to_model()

        # add comment to announcement

    def update_views(self, subject: User, slug: str) -> Announcement:
        """
        Increments the view count statistic of an announcement by 1 if the user requesting the change has not already viewed the announcement.

        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement

        Returns:
            Announcement: updated 'Announcement' object from the entity
        """

        announcement = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )

        if announcement is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        announcement.view_count += 1

        self._session.commit()

        return announcement.to_model()

    def update_shares(self, subject: User, slug: str) -> Announcement:
        """
        Increments the view count statistic of an announcement by 1 if the user requesting the change has not already viewed the announcement.

        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement

        Returns:
            Announcement: updated 'Announcement' object from the entity
        """

        announcement = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )

        if announcement is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        announcement.share_count += 1

        self._session.commit()

        return announcement.to_model()
