"""Tests for the AnnouncementService class"""

import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

from ....models.announcement import Announcement, AnnouncementStatus
from ....models.announcement_details import AnnouncementDetails
from ....models.announcement_comment import Comment
from ....services import AnnouncementService
from ..user_data import root, user
from .announcement_test_data import announcements

from ..fixtures import announcement_svc_integration

from ..core_data import setup_insert_data_fixture

import requests

__authors__ = ["Nicholas Sanaie"]


def test_get_all_published(announcement_svc_integration: AnnouncementService):
    published_announcements = announcement_svc_integration.all_published()
    assert published_announcements is not None
    assert len(published_announcements) == len(announcements) - 1
    assert isinstance(published_announcements[0], Announcement)


def test_get_by_slug_published(announcement_svc_integration: AnnouncementService):
    announcement = announcement_svc_integration.get_by_slug(announcements[0].slug)
    assert announcement is not None
    assert isinstance(announcement, AnnouncementDetails)
    assert announcement.slug == announcements[0].slug


def test_create_announcement_as_root(announcement_svc_integration: AnnouncementService):
    announcement = Announcement(
        id=0,
        headline="test",
        syn="test",
        body="test",
        author_id=1,
        slug="test",
        organization_id=1,
        image="test",
        status=AnnouncementStatus.DRAFT,
        view_count=0,
        share_count=0,
    )
    created_announcemeent = announcement_svc_integration.create(root, announcement)
    assert created_announcemeent is not None
    assert created_announcemeent.id is not None


def test_create_announcement_as_user(announcement_svc_integration: AnnouncementService):
    announcement = Announcement(
        id=0,
        headline="test",
        syn="test",
        body="test",
        author_id=1,
        slug="test",
        organization_id=1,
        image="test",
        status=AnnouncementStatus.DRAFT,
        view_count=0,
        share_count=0,
    )
    with pytest.raises(UserPermissionException):
        announcement_svc_integration.create(user, announcement)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_announcement_invalid_params(
    announcement_svc_integration: AnnouncementService,
):
    announcement = Announcement(
        id=0,
        headline="test",
        syn="test",
        body="test",
        author_id=1,
        slug="test",
        organization_id=0,
        image="test",
        status=AnnouncementStatus.DRAFT,
        view_count=0,
        share_count=0,
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.create(root, announcement)
        pytest.fail()  # Fail test if no error was thrown above
    announcement.organization_id = 1
    announcement.author_id = 0
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.create(root, announcement)
        pytest.fail()  # Fail test if no error was thrown above


def test_increment_announcement_views(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]
    old_views = announcement.view_count
    assert (
        announcement_svc_integration.update_views(user, announcement.slug).view_count
        == old_views + 1
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.update_views(user, "notarealslugever!")
        pytest.fail()


def test_increment_announcement_shares(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]
    old_shares = announcement.share_count
    assert (
        announcement_svc_integration.update_shares(user, announcement.slug).share_count
        == old_shares + 1
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.update_shares(user, "notarealslugever!")
        pytest.fail()


def test_create_comments(
    announcement_svc_integration: AnnouncementService,
):

    announcement = announcements[0]

    comment_1 = Comment(
        id=1,
        text="IM SO EXCITED!!!",
        author_id=1,
        posted_date="2024-04-16T15:33:25.326Z",
    )

    comment_2 = Comment(
        id=2, text="cant wait!", author_id=2, posted_date="2024-04-16T15:33:25.326Z"
    )

    created_comment = announcement_svc_integration.create_comment(
        user, announcement.slug, comment_1
    )
    assert created_comment is not None
    assert created_comment.id is not None

    updated_announcement = announcement_svc_integration.get_by_slug(announcement.slug)
    assert len(updated_announcement.comments) == 1

    announcement_svc_integration.create_comment(user, announcement.slug, comment_2)

    updated_announcement = announcement_svc_integration.get_by_slug(announcement.slug)
    assert len(updated_announcement.comments) == 2
