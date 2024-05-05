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
from .announcement_test_data import (
    announcements,
    published_announcements,
    admin_announcements,
)

from ..fixtures import announcement_svc_integration

from ..core_data import setup_insert_data_fixture

import requests

__authors__ = ["Nicholas Sanaie"]


def test_get_all_published(announcement_svc_integration: AnnouncementService):
    new_published_announcements = announcement_svc_integration.all_published()
    assert new_published_announcements is not None
    assert len(new_published_announcements) == len(published_announcements)
    assert isinstance(new_published_announcements[0], Announcement)


def test_get_all_admin(announcement_svc_integration: AnnouncementService):
    get_admin_announcements = announcement_svc_integration.all_admin(root)
    published_announcements = announcement_svc_integration.all_published()
    assert get_admin_announcements is not None
    assert published_announcements is not None
    assert len(get_admin_announcements) != len(published_announcements)
    assert len(get_admin_announcements) == len(admin_announcements)
    assert isinstance(admin_announcements[0], Announcement)
    assert announcements[5] not in admin_announcements


def test_get_by_slug_published(announcement_svc_integration: AnnouncementService):
    announcement = announcement_svc_integration.get_by_slug(announcements[0].slug)
    assert announcement is not None
    assert isinstance(announcement, AnnouncementDetails)
    assert announcement.slug == announcements[0].slug


def test_get_by_slug_not_found(announcement_svc_integration: AnnouncementService):
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.get_by_slug("notarealslugever!")
        pytest.fail()


def test_get_by_slug_not_published(announcement_svc_integration: AnnouncementService):
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.get_by_slug("pminterestdraft")
        pytest.fail()


def test_get_by_slug_published_admin(announcement_svc_integration: AnnouncementService):
    admin_announcement = announcement_svc_integration.get_by_slug_admin(
        root, announcements[0].slug
    )
    assert admin_announcement is not None
    assert isinstance(admin_announcement, AnnouncementDetails)
    assert admin_announcement.slug == announcements[0].slug


def test_get_by_slug_not_found_admin(announcement_svc_integration: AnnouncementService):
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.get_by_slug_admin(root, "notarealslugever!")
        pytest.fail()


def test_get_by_slug_archived_author_admin(
    announcement_svc_integration: AnnouncementService,
):
    admin_announcement = announcement_svc_integration.get_by_slug_admin(
        root, announcements[4].slug
    )
    assert admin_announcement is not None
    assert isinstance(admin_announcement, AnnouncementDetails)
    assert admin_announcement.slug == announcements[4].slug


def test_get_by_slug_drafted_author_admin(
    announcement_svc_integration: AnnouncementService,
):
    admin_announcement = announcement_svc_integration.get_by_slug_admin(
        root, announcements[3].slug
    )
    assert admin_announcement is not None
    assert isinstance(admin_announcement, AnnouncementDetails)
    assert admin_announcement.slug == announcements[3].slug


def test_get_by_slug_not_author_archived_admin(
    announcement_svc_integration: AnnouncementService,
):
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.get_by_slug_admin(root, "author-draft")
        pytest.fail()


def test_get_by_slug_not_author_draft_admin(
    announcement_svc_integration: AnnouncementService,
):
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.get_by_slug_admin(root, "not-author-draft")
        pytest.fail()


def test_create_announcement_as_root(announcement_svc_integration: AnnouncementService):
    announcement = Announcement(
        id=20,
        headline="test100",
        syn="test",
        body="test",
        author_id=1,
        slug="test100",
        organization_id=1,
        image="test",
        status=AnnouncementStatus.PUBLISHED,
        view_count=0,
        share_count=0,
    )
    announcement_2 = Announcement(
        id=21,
        headline="test101",
        syn="test",
        body="test",
        author_id=1,
        slug="test101",
        organization_id=1,
        status=AnnouncementStatus.PUBLISHED,
        view_count=0,
        share_count=0,
    )
    announcement_3 = Announcement(
        id=22,
        headline="test102",
        syn="test",
        body="test",
        author_id=1,
        slug="test102",
        status=AnnouncementStatus.PUBLISHED,
        view_count=0,
        share_count=0,
    )
    announcement_4 = Announcement(
        id=0,
        headline="test103",
        syn="test",
        body="test",
        author_id=1,
        slug="test103",
        status=AnnouncementStatus.PUBLISHED,
        view_count=0,
        share_count=0,
    )
    created_announcement = announcement_svc_integration.create(root, announcement)
    assert created_announcement is not None
    assert created_announcement.id is not None
    created_announcement = announcement_svc_integration.create(root, announcement_2)
    assert created_announcement is not None
    assert created_announcement.id is not None
    created_announcement = announcement_svc_integration.create(root, announcement_3)
    assert created_announcement is not None
    assert created_announcement.id is not None
    root.github_avatar = "https://avatars.githubusercontent.com/u/111389454?v=4"
    created_announcement = announcement_svc_integration.create(root, announcement_4)
    assert created_announcement is not None
    assert created_announcement.id is not None


def test_create_announcement_slug_already_exists(
    announcement_svc_integration: AnnouncementService,
):
    announcement = Announcement(
        id=0,
        headline="test",
        syn="test",
        body="test",
        author_id=1,
        slug="appteamapps",
        organization_id=1,
        image="test",
        status=AnnouncementStatus.DRAFT,
        view_count=0,
        share_count=0,
    )
    with pytest.raises(ResourceNotFoundException):
        created_announcement = announcement_svc_integration.create(root, announcement)
        pytest.fail()


def test_delete_announcement(
    announcement_svc_integration: AnnouncementService,
):
    announcement_svc_integration.delete(root, "appteamapps")
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.get_by_slug_admin(root, "appteamapps")
        pytest.fail()
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.delete(root, "notarealslug!")
        pytest.fail()


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
        pytest.fail()


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
        upvote_count=0,
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.create(root, announcement)
        pytest.fail()
    announcement.organization_id = 1
    announcement.author_id = 0
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.create(root, announcement)
        pytest.fail()


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


def test_add_announcement_favorite(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]

    assert (
        announcement_svc_integration.add_favorite(user, announcement.slug).upvoted
        == True
    )
    assert (
        announcement_svc_integration.add_favorite(user, announcement.slug).upvoted
        == True
    )

    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.add_favorite(user, "notarealslugever!")
        pytest.fail()


def test_remove_announcement_favorite(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]

    assert (
        announcement_svc_integration.remove_favorite(user, announcement.slug).upvoted
        == False
    )
    announcement_svc_integration.add_favorite(user, announcement.slug)
    assert (
        announcement_svc_integration.remove_favorite(user, announcement.slug).upvoted
        == False
    )

    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.remove_favorite(user, "notarealslugever!")
        pytest.fail()


def test_check_announcement_favorites(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]
    assert (
        announcement_svc_integration.add_favorite(user, announcement.slug).upvoted
        == True
    )
    assert (
        announcement_svc_integration.check_favorite(user, announcement.slug).upvoted
        == True
    )
    assert (
        announcement_svc_integration.remove_favorite(user, announcement.slug).upvoted
        == False
    )
    assert (
        announcement_svc_integration.check_favorite(user, announcement.slug).upvoted
        == False
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.check_favorite(user, "notarealslugever!")
        pytest.fail()


def test_increment_announcement_upvotes(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]
    old_upvotes = announcement.upvote_count
    assert (
        announcement_svc_integration.add_upvote(user, announcement.slug).upvoted == True
    )
    assert (
        announcement_svc_integration.get_by_slug(announcement.slug).upvote_count
        == old_upvotes + 1
    )
    assert (
        announcement_svc_integration.add_upvote(user, announcement.slug).upvoted == True
    )
    assert (
        announcement_svc_integration.get_by_slug(announcement.slug).upvote_count
        == old_upvotes + 1
    )

    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.add_upvote(user, "notarealslugever!")
        pytest.fail()


def test_decrement_announcement_upvotes(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]
    old_upvotes = announcement.upvote_count
    assert (
        announcement_svc_integration.add_upvote(user, announcement.slug).upvoted == True
    )
    old_upvotes = announcement_svc_integration.get_by_slug(
        announcement.slug
    ).upvote_count
    assert (
        announcement_svc_integration.remove_upvote(user, announcement.slug).upvoted
        == False
    )
    assert (
        announcement_svc_integration.get_by_slug(announcement.slug).upvote_count
        == old_upvotes - 1
    )
    assert (
        announcement_svc_integration.remove_upvote(user, announcement.slug).upvoted
        == False
    )
    assert (
        announcement_svc_integration.get_by_slug(announcement.slug).upvote_count
        == old_upvotes - 1
    )

    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.remove_upvote(user, "notarealslugever!")
        pytest.fail()


def test_check_announcement_upvotes(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]
    old_upvotes = announcement.upvote_count
    assert (
        announcement_svc_integration.add_upvote(user, announcement.slug).upvoted == True
    )
    assert (
        announcement_svc_integration.check_upvote(user, announcement.slug).upvoted
        == True
    )
    assert (
        announcement_svc_integration.remove_upvote(user, announcement.slug).upvoted
        == False
    )
    assert (
        announcement_svc_integration.check_upvote(user, announcement.slug).upvoted
        == False
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.check_upvote(user, "notarealslugever!")
        pytest.fail()


def test_update_announcement(
    announcement_svc_integration: AnnouncementService,
):
    updated_announcement = Announcement(
        id=2,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=1,
        slug="pminterest",
        organization_id=2,
        image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pm.jpg",
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    before = announcement_svc_integration.get_by_slug("pminterest")
    after = announcement_svc_integration.update_announcement(root, updated_announcement)

    assert before != updated_announcement
    assert before != after
    assert after.id == updated_announcement.id
    assert after.headline == updated_announcement.headline
    assert after.syn == updated_announcement.syn
    assert after.body == updated_announcement.body
    assert after.status == updated_announcement.status
    assert after.image == updated_announcement.image


def test_update_announcement_wrong_id(
    announcement_svc_integration: AnnouncementService,
):
    updated_announcement = Announcement(
        id=243,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=1,
        slug="pminterest",
        organization_id=2,
        image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pm.jpg",
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.update_announcement(root, updated_announcement)
        pytest.fail()
    updated_announcement = Announcement(
        id=2,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=1,
        slug="pminterest",
        organization_id=123,
        image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pm.jpg",
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.update_announcement(root, updated_announcement)
        pytest.fail()


def test_update_announcement_not_author(
    announcement_svc_integration: AnnouncementService,
):
    updated_announcement = Announcement(
        id=6,
        headline="UPDATED",
        syn="Positions open for project and education members",
        body="Positions open for project and education members. Apply for KTP Club by Feb 9 to work on one of our project teams.",
        author_id=2,
        slug="author-draft",
        organization_id=2,
        image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/ktp.png",
        status=AnnouncementStatus.ARCHIVED,
        view_count=0,
        share_count=0,
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.update_announcement(root, updated_announcement)
        pytest.fail()


def test_update_announcement_status(
    announcement_svc_integration: AnnouncementService,
):
    updated_announcement = Announcement(
        id=4,
        headline="ACM Club interest meeting",
        syn="Positions open for project and education members",
        body="Positions open for project and education members. Apply for ACM Club by Feb 9 to work on one of our project teams.",
        author_id=1,
        slug="pminterestdraft",
        organization_id=2,
        image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/acm.jpg",
        status=AnnouncementStatus.PUBLISHED,
        view_count=0,
        share_count=0,
    )
    assert (
        updated_announcement.status
        == announcement_svc_integration.update_announcement(
            root, updated_announcement
        ).status
    )
    updated_announcement.status = AnnouncementStatus.ARCHIVED
    assert (
        updated_announcement.status
        == announcement_svc_integration.update_announcement(
            root, updated_announcement
        ).status
    )
    assert (
        updated_announcement.status
        == announcement_svc_integration.update_announcement(
            root, updated_announcement
        ).status
    )


def test_update_announcement_image(
    announcement_svc_integration: AnnouncementService,
):
    updated_announcement = Announcement(
        id=2,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=1,
        slug="pminterest",
        organization_id=2,
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    assert (
        announcement_svc_integration.update_announcement(root, updated_announcement).id
        == updated_announcement.id
    )
    announcement = announcement_svc_integration.get_by_slug("pminterest")
    assert announcement.image == announcement.organization.logo

    updated_announcement = Announcement(
        id=2,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=1,
        slug="pminterest",
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    assert (
        announcement_svc_integration.update_announcement(root, updated_announcement).id
        == updated_announcement.id
    )
    announcement = announcement_svc_integration.get_by_slug("pminterest")
    assert announcement.image == announcement.author.github_avatar


def test_update_announcement_new_slug_id(
    announcement_svc_integration: AnnouncementService,
):
    updated_announcement = Announcement(
        id=2,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=1,
        slug="newslug",
        organization_id=2,
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    assert (
        updated_announcement.id
        == announcement_svc_integration.update_announcement(
            root, updated_announcement
        ).id
    )
    updated_announcement = Announcement(
        id=123,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=1,
        slug="newslug",
        organization_id=2,
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.update_announcement(root, updated_announcement)
        pytest.fail()


def test_update_announcement_wrong_author(
    announcement_svc_integration: AnnouncementService,
):
    updated_announcement = Announcement(
        id=2,
        headline="UPDATED",
        syn="UPDATED",
        body="UPDATED",
        author_id=12345,
        slug="newslug",
        organization_id=2,
        status=AnnouncementStatus.PUBLISHED,
        view_count=1,
        share_count=1,
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.update_announcement(root, updated_announcement)
        pytest.fail()


def test_create_comments(
    announcement_svc_integration: AnnouncementService,
):

    announcement = announcements[0]

    comment_1 = Comment(
        id=1,
        text="IM SO EXCITED!!!",
        author_id=1,
    )

    comment_2 = Comment(id=2, text="cant wait!", author_id=2)

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

    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.create_comment(
            root, "notarealslugever!", comment_2
        )
        pytest.fail()


def test_create_comment_wrong_author(
    announcement_svc_integration: AnnouncementService,
):
    announcement = announcements[0]
    comment = Comment(id=1, text="IM SO EXCITED!!!", author_id=0)
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.create_comment(user, announcement.slug, comment)
        pytest.fail()


def test_create_comment_missing_announcement(
    announcement_svc_integration: AnnouncementService,
):
    comment = Comment(
        id=1,
        text="IM SO EXCITED!!!",
        author_id=1,
        posted_date="2024-04-16T15:33:25.326Z",
    )
    with pytest.raises(ResourceNotFoundException):
        announcement_svc_integration.create_comment(user, "notarealslugever!", comment)
        pytest.fail()
