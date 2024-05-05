"""
This Announcements Service is for use with the API to create, edit and delete announcement data in the database.
"""

from fastapi import Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from ..database import db_session
from ..models.announcement import Announcement, AnnouncementStatus
from ..models.announcement_comment import Comment
from ..models.announcement_details import AnnouncementDetails, UpvoteBoolean
from ..entities.announcement_entity import AnnouncementEntity
from ..entities.announcements_comment_entity import AnnouncementCommentEntity
from ..entities.organization_entity import OrganizationEntity
from ..entities.user_entity import UserEntity
from ..models import User
from .permission import PermissionService

from .exceptions import ResourceNotFoundException, UserPermissionException

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

    def all_admin(self, subject: User) -> list[Announcement]:
        """
        Retrieves all announcements from the table that should be visible for admin: published, archived, and draft with corresponding author id.

        Returns:
            list[Announcement]: List of all `Announcements` visible to admin
        """

        self._permission.enforce(subject, "announcement.create", f"announcement")

        entities = (
            self._session.query(AnnouncementEntity)
            .where(
                (AnnouncementEntity.status == AnnouncementStatus.PUBLISHED)
                | (
                    (AnnouncementEntity.status == AnnouncementStatus.ARCHIVED)
                    & (subject.id == AnnouncementEntity.author_id)
                )
                | (
                    (AnnouncementEntity.status == AnnouncementStatus.DRAFT)
                    & (subject.id == AnnouncementEntity.author_id)
                )
            )
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

    def get_by_slug_admin(self, subject: User, slug: str) -> AnnouncementDetails:
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

        if (
            announcement.status == AnnouncementStatus.ARCHIVED
            and subject.id != announcement.author_id
        ):
            raise ResourceNotFoundException(
                "Announcement exists, but you do not have permission to view it."
            )

        if (
            announcement.status == AnnouncementStatus.DRAFT
            and subject.id != announcement.author_id
        ):
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

        organization_entity = (
            self._session.query(OrganizationEntity)
            .filter_by(id=announcement.organization_id)
            .first()
        )
        author_entity = (
            self._session.query(UserEntity).filter_by(id=announcement.author_id).first()
        )

        if not author_entity:
            raise ResourceNotFoundException(
                "Author user does not exist in the database."
            )

        if announcement.organization_id is not None and not organization_entity:
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

        if announcement.image is None:
            if organization_entity and organization_entity.logo:
                announcement.image = organization_entity.logo
            elif author_entity and author_entity.github_avatar:
                announcement.image = author_entity.github_avatar

        if announcement.status == AnnouncementStatus.PUBLISHED:
            announcement.published_date = datetime.now()

        announcement_entity = AnnouncementEntity.from_model(announcement)
        self._session.add(announcement_entity)
        self._session.commit()

        return announcement_entity.to_model()

    def delete(self, subject: User, slug: str) -> None:
        """
        Delete the announcement based on the provided slug.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            slug: a string representing a unique announcement slug

        Raises:
            ResourceNotFoundException: If no announcement is found with the corresponding slug
        """
        # Check if user has admin permissions
        self._permission.enforce(subject, "announcement.delete", f"announcement")

        # Find object to delete
        obj = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )

        # Ensure object exists
        if obj is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        self._session.delete(obj)
        
        self._session.commit()

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
        author_from_id = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == comment.author_id)
            .one_or_none()
        )

        if author is None or author_from_id is None:
            raise ResourceNotFoundException("User does not exist in the database.")

        comment.posted_date = None
        comment.posted_date = datetime.now()

        comment_entity = AnnouncementCommentEntity.from_model(comment)
        announcement.comments.append(comment_entity)
        self._session.commit()

        return comment_entity.to_model()

    def update_announcement(
        self, subject: User, announcement: Announcement
    ) -> Announcement:
        """
        Retrieves an announcement entity with corresponding id and returns new announcement model with updated fields

        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement

        Returns:
            Announcement: updated 'Announcement' object from the entity
        """
        # Check if user has admin permissions

        self._permission.enforce(subject, "announcement.update", f"announcement")

        organization_entity = (
            self._session.query(OrganizationEntity)
            .filter_by(id=announcement.organization_id)
            .first()
        )
        author_entity = (
            self._session.query(UserEntity).filter_by(id=announcement.author_id).first()
        )

        if not author_entity:
            raise ResourceNotFoundException(
                "Author user does not exist in the database."
            )

        if announcement.organization_id is not None and not organization_entity:
            raise ResourceNotFoundException(
                "Organization does not exist in the database."
            )

        announcement_entity = (
            self._session.get(AnnouncementEntity, announcement.id)
            if announcement.id
            else None
        )

        if announcement_entity is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching ID: {announcement.id}"
            )

        if (
            announcement_entity.status != AnnouncementStatus.PUBLISHED
            and subject.id != announcement_entity.author_id
        ):
            raise ResourceNotFoundException(
                f"No announcement found with matching ID: {announcement.id}"
            )

        if announcement.image is None:
            if organization_entity and organization_entity.logo:
                announcement.image = organization_entity.logo
            elif author_entity and author_entity.github_avatar:
                announcement.image = author_entity.github_avatar

        if announcement.status == AnnouncementStatus.PUBLISHED:
            if announcement_entity.status == AnnouncementStatus.PUBLISHED:
                announcement.modified_date = datetime.now()
            else:
                announcement.published_date = datetime.now()
        if announcement.status == AnnouncementStatus.ARCHIVED:
            if announcement_entity.status == AnnouncementStatus.ARCHIVED:
                announcement.modified_date = datetime.now()
            else:
                announcement.archived_date = datetime.now()

        announcement_entity.headline = announcement.headline
        announcement_entity.syn = announcement.syn
        announcement_entity.body = announcement.body
        announcement_entity.slug = announcement.slug
        if announcement.organization_id is not None:
            announcement_entity.organization_id = announcement.organization_id
        announcement_entity.status = announcement.status
        if announcement.image:
            announcement_entity.image_url = announcement.image
        if announcement.modified_date:
            announcement_entity.modified_date = announcement.modified_date
        if announcement.published_date:
            announcement_entity.published_date = announcement.published_date
        if announcement.archived_date:
            announcement_entity.archived_date = announcement.archived_date
        self._session.commit()

        return announcement_entity.to_model()

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

    def add_upvote(self, subject: User, slug: str) -> Announcement:
        """
        Increments the upvote statistic of an announcement by 1 if the user requesting the change has not already upvoted the announcement.

        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement

        Returns:
            Announcement: updated 'Announcement' object from the entity
        """

        announcement_entity = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )
        subject_entity = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == subject.id)
            .one_or_none()
        )

        if announcement_entity is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        if subject_entity.upvote_announcement(announcement_entity):
            announcement_entity.upvote_count += 1

        self._session.commit()

        return UpvoteBoolean(upvoted=True)

    def remove_upvote(self, subject: User, slug: str) -> Announcement:
        """
        Decrements the upvote statistic of an announcement by 1 if the user requesting the change has upvoted the announcement.

        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement

        Returns:
            Announcement: updated 'Announcement' object from the entity
        """

        announcement_entity = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )
        subject_entity = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == subject.id)
            .one_or_none()
        )

        if announcement_entity is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        if subject_entity.remove_upvote_announcement(announcement_entity):
            announcement_entity.upvote_count -= 1

        self._session.commit()

        return UpvoteBoolean(upvoted=False)

    def check_upvote(self, subject: User, slug: str) -> Announcement:
        """
        Checks if the subject has upvoted the announcement with the given slug.

        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement

        Returns:
            upvoted: a boolean that is True if user has upvoted and false if not
        """

        announcement_entity = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )
        subject_entity = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == subject.id)
            .one_or_none()
        )

        if announcement_entity is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        return UpvoteBoolean(
            upvoted=subject_entity.check_upvote_announcement(announcement_entity)
        )

    def add_favorite(self, subject: User, slug: str) -> UpvoteBoolean:
        """
        Adds the announcement at the given slug to the user favorite data.


        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement


        Returns:
            UpvoteBoolean: a model that contains the boolean for the current status of the statistic
        """

        announcement_entity = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )
        subject_entity = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == subject.id)
            .one_or_none()
        )

        if announcement_entity is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        if announcement_entity not in subject_entity.announcement_favorites:
            subject_entity.announcement_favorites.append(announcement_entity)

        self._session.commit()

        return UpvoteBoolean(upvoted=True)

    def remove_favorite(self, subject: User, slug: str) -> UpvoteBoolean:
        """
        Removes the announcement at the given slug from the user favorite announcement data.


        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement


        Returns:
            UpvoteBoolean: a model that contains the boolean for the current status of the statistic
        """

        announcement_entity = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )
        subject_entity = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == subject.id)
            .one_or_none()
        )

        if announcement_entity is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        if announcement_entity in subject_entity.announcement_favorites:
            subject_entity.announcement_favorites.remove(announcement_entity)

        self._session.commit()

        return UpvoteBoolean(upvoted=False)

    def check_favorite(self, subject: User, slug: str) -> UpvoteBoolean:
        """
        Checks if the subject has favorited the announcement with the given slug.


        Parameters:
            subject: a valid User model represnting the currently logged in User
            slug: a unique string representing a unique announcement


        Returns:
            UpvoteBoolean: a model that contains the boolean for the current status of the statistic
        """

        announcement_entity = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )
        subject_entity = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == subject.id)
            .one_or_none()
        )

        if announcement_entity is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        return UpvoteBoolean(
            upvoted=announcement_entity in subject_entity.announcement_favorites
        )
