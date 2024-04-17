"""Announcement API

Announcemnts routes are used to create, retrieve, update and delete annoumcenets."""

from fastapi import APIRouter, Depends

from ..services import AnnouncementService
from ..models.announcement import Announcement
from ..models.announcement_details import AnnouncementDetails
from ..models.announcement_comment import Comment
from ..models.user import User
from ..api.authentication import registered_user

__authors__ = ["Nicholas Sanaie", "Mark Maio", "Tanner Macpherson", "Tyler Roth"]

api = APIRouter(prefix="/api/announcements")
openapi_tags = {
    "name": "Announcements",
    "description": "Create, retrieve, update and delete CS Department announcements.",
}


@api.get("", response_model=list[Announcement], tags=["Announcements"])
def get_published_announcements(
    announcement_service: AnnouncementService = Depends(),
) -> list[Announcement]:
    """
    Get all published and public announcements.

    Parameters:
        announcement_service: a valid AnnouncementService

    Returns:
        list[Announcement]: All published `Announcement`s in the database table
    """

    return announcement_service.all_published()


@api.get("/admin", response_model=list[Announcement], tags=["Announcements"])
def get_admin_announcements(
    subject: User = Depends(registered_user),
) -> list[Announcement]:
    """
    Get all announcements that the user is authorized to view.

    Returns:
        list[Announcement]: All `Announcement`s in database table that the user is authorized to view.
    """

    # return announcement_service.all_admin(subject)


@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=AnnouncementDetails,
    tags=["Announcements"],
)
def get_announcement(
    slug: str, announcement_service: AnnouncementService = Depends()
) -> AnnouncementDetails:
    """
    Get announcement with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Announcement

    Returns:
        AnnouncementDetails: AnnouncementDetails object with matching slug

    Raises:
        HTTPException 404 if get_by_slug() raises an Exception
    """

    return announcement_service.get_by_slug(slug)


@api.get(
    "/admin/{slug}",
    responses={404: {"model": None}},
    response_model=AnnouncementDetails,
    tags=["Announcements"],
)
def get_announcement(
    slug: str,
    announcement_service: AnnouncementService = Depends(),
    subject: User = Depends(registered_user),
) -> AnnouncementDetails:
    """
    Get announcement with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Announcement
        subject: a valid User model representing the currently logged in User

    Returns:
        AnnouncementDetails: AnnouncementDetails object with matching slug

    Raises:
        HTTPException 404 if get_by_slug() raises an Exception
    """

    # return announcement_service.get_by_slug_admin(subject, slug)
    # TODO: add this to deisgn doc


@api.post("", response_model=Announcement, tags=["Announcements"])
def new_announcement(
    announcement: Announcement,
    announcement_service: AnnouncementService = Depends(),
    subject: User = Depends(registered_user),
) -> Announcement:
    """
    Create announcement

    Parameters:
        announcement: a valid Announcement model
        announcement_service: a valid AnnouncementService
        subject: a valid User model representing the currently logged in User

    Returns:
        Announcement: Created announcement

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    return announcement_service.create(subject, announcement)


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


@api.put("/{slug}/viewCount", response_model=Announcement, tags=["Announcements"])
def increment_views(
    slug: str,
    subject: User = Depends(registered_user),
    announcement_service: AnnouncementService = Depends(),
) -> Announcement:
    """
    Increment the announcement view count

    Parameters:
        slug: a string reprsenting a unique identifier for an Announcement
        subject: a valid User model representing the currently logged in User
        announcement_service: a valid AnnouncementService

    Returns:
        Announcement: Updated announcement

    Raises:
        HTTPException 404 if update_views() raises an Exception
    """

    return announcement_service.update_views(subject, slug)


@api.put("/{slug}/shareCount", response_model=Announcement, tags=["Announcements"])
def increment_shares(
    slug: str,
    subject: User = Depends(registered_user),
    announcement_service: AnnouncementService = Depends(),
) -> Announcement:
    """
    Increment the announcement share count

    Parameters:
        slug: a string reprsenting a unique identifier for an Announcement
        subject: a valid User model representing the currently logged in User
        announcement_service: a valid AnnouncementService

    Returns:
        Announcement: Updated announcement

    Raises:
        HTTPException 404 if update_views() raises an Exception
    """

    return announcement_service.update_shares(subject, slug)


@api.post("/{slug}/comments", response_model=Comment, tags=["Announcements"])
def new_comment(
    slug: str,
    comment: Comment,
    subject: User = Depends(registered_user),
    announcement_service: AnnouncementService = Depends(),
) -> Comment:
    """
    Create comment for a specific announcement

    Parameters:
        slug: a string representing a unique identifier for an Announcement
        comment: a valid Comment model
        subject: a valid User model representing the currently logged in User
        announcement_service: a valid AnnouncementService

    Returns:
        Comment: Created comment

    Raises:
        HTTPException 422 if create_comment() raises an Exception
    """

    return announcement_service.create_comment(subject, slug, comment)


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
