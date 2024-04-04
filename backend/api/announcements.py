"""Announcement API

Announcemnts routes are used to create, retrieve, update and delete annoumcenets."""

from fastapi import APIRouter, Depends

from ..models.announcement import Announcement
from ..models.announcement_comment import Comment
from ..models.user import User
from ..api.authentication import registered_user

from ..services import OrganizationService

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tanner Macpherson", "Tyler Roth"]

api = APIRouter(prefix="/api/announcements")
openapi_tags = {
    "name": "Announcements",
    "description": "Create, retrieve, update and delete CS Department announcements.",
}


@api.get("", response_model=list[Announcement], tags=["Announcements"])
def get_announcements() -> list[Announcement]:
    """
    Get all announcements.

    Returns:
        list[PublishedAnnouncement]: All `PublishedAnnouncements`s in the `Announcements` database table
    """

    # return announcement_service.all()


@api.get(
    "/{slug_id}",
    responses={404: {"model": None}},
    response_model=Announcement,
    tags=["Announcements"],
)
def get_announcement(slug_id: str) -> Announcement:
    """
    Get announcement with matching slug

    Parameters:
        slug_id: a string representing a unique identifier for an Announcement

    Returns:
        Announcement: Announcement with matching slug

    Raises:
        HTTPException 404 if get_by_slug() raises an Exception
    """

    # return announcement_service.get_by_slug(slug)


@api.post("", response_model=Announcement, tags=["Announcements"])
def new_announcement(
    announcement: Announcement, subject: User = Depends(registered_user)
) -> Announcement:
    """
    Create announcement

    Parameters:
        announcement: a valid Announcement model
        subject: a valid User model representing the currently logged in User

    Returns:
        Announcement: Created announcement

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    # return announcement_service.create(subject, announcement)


@api.put(
    "/",
    responses={404: {"model": None}},
    response_model=Announcement,
    tags=["Announcements"],
)
def update_announcement(
    announcement: Announcement,
    subject: User = Depends(registered_user),
) -> Announcement:
    """
    Update announcement

    Parameters:
        announcement: a valid Announcement model
        subject: a valid User model representing the currently logged in User

    Returns:
        Announcement: Updated announcement

    Raises:
        HTTPException 404 if update() raises an Exception
    """

    # return announcement_service.update(subject, announcement)


@api.delete("/{slug_id}", response_model=None, tags=["Announcements"])
def delete_announcement(
    slug_id: str,
    subject: User = Depends(registered_user),
):
    """
    Delete announcement based on slug

    Parameters:
        slug_id: a string representing a unique identifier for an Announcement
        subject: a valid User model representing the currently logged in User

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    # announcement_service.delete(subject, slug)


@api.post("/{slug_id}/comments", response_model=Comment, tags=["Announcements"])
def new_comment(comment: Comment, subject: User = Depends(registered_user)) -> Comment:
    """
    Create comment for a specific announcement

    Parameters:
        comment: a valid Comment model
        subject: a valid User model representing the currently logged in User

    Returns:
        Comment: Created comment

    Raises:
        HTTPException 422 if create_comment() raises an Exception
    """

    # announcement_service.create_comment(subject, slug)


@api.delete(
    "/comments/{slug_id}/{comment_id}", response_model=None, tags=["Announcements"]
)
def delete_comment(
    slug_id: str,
    comment_id: int,
    subject: User = Depends(registered_user),
):
    """
    Delete a comment for the announcement at the slug_id

    Parameters:
        slug_id: a string representing a unique identifier for an Announcement
        comment_id: a int representing a unique indetifier for a comment
        subject: a valid User model representing the currently logged in User

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    # announcement_service.delete_comment(subject, slug)
