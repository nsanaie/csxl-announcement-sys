"""Contains mock data for to run tests on the announcements feature."""

import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from ....models.announcement import Announcement, AnnouncementStatus
from ....models.announcement_details import AnnouncementDetails
from ....entities.announcement_entity import AnnouncementEntity

from ..organization.organization_demo_data import organizations
from ..organization.organization_test_data import insert_fake_data

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Nicholas Sanaie"]

# sample announcement objects

announcement_1 = Announcement(
    id=1,
    headline="Apply for App Team Carolina!",
    syn="Applications are OUT for the Spring semester! Apply by March 1st.",
    body="Apply to join App Team Carolina on our website: https://appteamcarolina.com/. Applications are due September 4, by 11:59 PM. If you have any questions or would like more information, feel free to reach out to me at x@ad.unc.edu.",
    author_id=2,
    slug="appteamapps",
    organization_id=1,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/appteam.jpg",
    status=AnnouncementStatus.PUBLISHED,
    view_count=25,
    share_count=5,
)

announcement_2 = Announcement(
    id=2,
    headline="CSSG interest meeting",
    syn="Positions open for project and education members",
    body="Positions open for project and education members. Apply for CSSG by Feb 9 to work on one of our project teams.",
    author_id=1,
    slug="pminterest",
    organization_id=2,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pm.jpg",
    status=AnnouncementStatus.PUBLISHED,
    view_count=1,
    share_count=1,
)

announcement_3 = Announcement(
    id=3,
    headline="CSSG interest meeting",
    syn="Positions open for project and education members",
    body="Positions open for project and education members. Apply for CSSG by Feb 9 to work on one of our project teams.",
    author_id=1,
    slug="test1",
    organization_id=2,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pm.jpg",
    status=AnnouncementStatus.DRAFT,
    view_count=0,
    share_count=0,
)

announcement_4 = Announcement(
    id=4,
    headline="ACM Club interest meeting",
    syn="Positions open for project and education members",
    body="Positions open for project and education members. Apply for ACM Club by Feb 9 to work on one of our project teams.",
    author_id=1,
    slug="pminterestdraft",
    organization_id=2,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/acm.jpg",
    status=AnnouncementStatus.DRAFT,
    view_count=0,
    share_count=0,
)

announcement_5 = Announcement(
    id=5,
    headline="GWC Club interest meeting",
    syn="Positions open for project and education members",
    body="Positions open for project and education members. Apply for GWC Club by Feb 9 to work on one of our project teams.",
    author_id=1,
    slug="broke",
    organization_id=2,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/gwc.png",
    status=AnnouncementStatus.ARCHIVED,
    view_count=0,
    share_count=0,
)

announcement_6 = Announcement(
    id=6,
    headline="KTP Club interest meeting",
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

announcement_7 = Announcement(
    id=7,
    headline="ACM Club interest meeting",
    syn="Positions open for project and education members",
    body="Positions open for project and education members. Apply for ACM Club by Feb 9 to work on one of our project teams.",
    author_id=2,
    slug="not-author-draft",
    organization_id=2,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/acm.jpg",
    status=AnnouncementStatus.DRAFT,
    view_count=0,
    share_count=0,
)

published_announcements = [announcement_1, announcement_2]
announcements = [
    announcement_1,
    announcement_2,
    announcement_3,
    announcement_4,
    announcement_5,
    announcement_6,
    announcement_7,
]
admin_announcements = [
    announcement_1,
    announcement_2,
    announcement_3,
    announcement_4,
    announcement_5,
]


def insert_fake_data(session: Session):
    """Inserts fake announcement data into the test session."""

    global announcements

    # Create entities for test organization data
    entities = []
    for ann in announcements:
        if ann.status == AnnouncementStatus.PUBLISHED:
            ann.published_date = datetime.now()
        entity = AnnouncementEntity.from_model(ann)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, AnnouncementEntity, AnnouncementEntity.id, len(announcements) + 1
    )

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
