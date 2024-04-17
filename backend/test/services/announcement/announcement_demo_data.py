"""Contains mock data for the live demo of the organizations feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.announcement import Announcement, AnnouncementStatus
from ....models.announcement_comment import Comment
from ....entities.announcement_entity import AnnouncementEntity
from ....entities.announcements_comment_entity import AnnouncementCommentEntity

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Nicholas Sanaie"]

announcement_1 = Announcement(
    id=1,
    headline="Apply for App Team Carolina!",
    syn="Applications are OUT for the Spring semester! Apply by March 1st.",
    body="""Hi CS Majors! 
 
         Are you interested in app development and design? Eager to dive into the world of app creation and innovation? Look no further! App Team Carolina, UNC’s student app development team, is now recruiting! 
         Whether you're a seasoned developer or just getting started, our organization offers a supportive and collaborative environment for anyone and everyone! 
 
🌟 What We Offer: 
- Learn from Experts:  Join our teams led by experienced app developers and designers who are ready to share their insights, tips, and best practices. 
- Collaborative Projects:  Join forces with fellow students to build real-world mobile applications, collaborating closely with developers, product managers, marketers, and designers. From concept to deployment, you'll experience the entire app development lifecycle. 
- Industry Partners: Get inspired by industry professionals sharing their journeys, experiences, and valuable tips within the realm of app development. 

👥 Who We Are Looking For:
- Product Manager 
- Product Marketing Manager 
- Graphic Designer 
- UI/UX Designer 
- UI/UX Trainee 
- Backend Developer 
- Android Developer  
- iOS Developer  
- iOS Trainee 

**Apply to join App Team Carolina on our website: https://appteamcarolina.com/. Applications are due September 4, by 11:59 PM. If you have any questions or would like more information, feel free to reach out to me at wastilla@ad.unc.edu.**

Best, 

Will Astilla  
Chief Marketing Officer 
App Team Carolina """,
    author_id=2,
    slug="appteamapps",
    organization_id=1,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/appteam.jpg",
    status=AnnouncementStatus.PUBLISHED,
    view_count=25,
    share_count=5,
    published_date="April 13, 2024 at 11:00am",
)

announcement_2 = Announcement(
    id=2,
    headline="CS+SG Career Trek Applications Open!",
    syn="Computer Science + Social Good (CS+SG) is having a career trek at the Google headquarters in Durham on April 24th (tentatively) from 10am to 2pm!",
    body="""During this career trek, students will have the opportunity to network with employees at Google (including the Eastern regional recruiter!), learn about the culture at Google, and even get exclusive insight on Google’s upcoming job and internship openings!! 
    
    This opportunity is open to all students, and we encourage everyone to apply to attend before the application closes on April 12, 2024 at 11:59pm.

    
    Food and transportation will be provided!

    Application: https://forms.gle/dhtysxEEzetSupjU6

    Questions or concerns? Email CS+SG at cssgunc@gmail.com.""",
    author_id=1,
    slug="cssgtrek",
    organization_id=6,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cssg.png",
    status=AnnouncementStatus.PUBLISHED,
    view_count=1,
    share_count=1,
    published_date="April 14, 2024 at 11:30am",
)

announcement_3 = Announcement(
    id=3,
    headline="CS+SG Career Trek Applications Open!",
    syn="Computer Science + Social Good (CS+SG) is having a career trek at the Google headquarters in Durham on April 24th (tentatively) from 10am to 2pm!",
    body="""During this career trek, students will have the opportunity to network with employees at Google (including the Eastern regional recruiter!), learn about the culture at Google, and even get exclusive insight on Google’s upcoming job and internship openings!! 
    
    This opportunity is open to all students, and we encourage everyone to apply to attend before the application closes on April 12, 2024 at 11:59pm.

    
    Food and transportation will be provided!

    Application: https://forms.gle/dhtysxEEzetSupjU6

    Questions or concerns? Email CS+SG at cssgunc@gmail.com.""",
    author_id=1,
    slug="cssgtrekdraft",
    organization_id=6,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cssg.png",
    status=AnnouncementStatus.DRAFT,
    view_count=0,
    share_count=0,
)

announcement_4 = Announcement(
    id=4,
    headline="Resume Workshop (February 28th)",
    syn="Resume workshop for aspiring SWEs, DS and PMs!",
    body="""Dear UNC students,

We are excited to announce an upcoming Resume Workshop designed to help you craft the perfect resume and stand out in your job applications! Whether you're a student, a recent graduate, or a professional looking to take the next step in your career, this workshop is for you.

Workshop Details:

Date: 4/20/24
Time: 12:00pm
Location: Sitterson (or online if virtual)
RSVP: Please RSVP by [RSVP Deadline] to secure your spot!
What You Will Learn:

- How to tailor your resume for different job opportunities
- Tips for showcasing your skills and experiences effectively
- Strategies for using keywords to pass applicant tracking systems (ATS)
- Best practices for formatting and organizing your resume
- Real-life examples and templates to get you started

What to Bring:

A copy of your current resume (if you have one)
A notebook and pen for taking notes
During the workshop, our expert facilitator will guide you through the process of creating a compelling resume that highlights your strengths and achievements. There will also be an opportunity for one-on-one feedback and Q&A sessions.

This workshop is a fantastic opportunity to enhance your resume and increase your chances of landing your dream job. We encourage you to join us for this informative and interactive session.

To RSVP, please reply to this email or contact us at [Contact Information].

We look forward to seeing you at the workshop!

Best regards,

[Your Name]
[Your Title/Organization]
[Contact Information]""",
    author_id=1,
    slug="resume",
    organization_id=4,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
    status=AnnouncementStatus.PUBLISHED,
    view_count=1,
    share_count=1,
    published_date="Apr 16th, 2024 at 12:24 PM",
)

announcements = [
    announcement_1,
    announcement_2,
    announcement_3,
    announcement_4,
]


comment_1 = Comment(
    id=1,
    text="IM SO EXCITED!!!",
    author_id=1,
    posted_date="2024-04-16T15:33:25.326Z",
)

comment_2 = Comment(
    id=2, text="cant wait!", author_id=2, posted_date="2024-04-16T15:33:25.326Z"
)

comments = [comment_1, comment_2]


def insert_fake_data(session: Session):
    """Inserts fake announcements data into the test session."""

    global announcements

    # Create entities for test organization data
    entities = []
    for ann in announcements:
        entity = AnnouncementEntity.from_model(ann)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, AnnouncementEntity, AnnouncementEntity.id, len(announcements) + 1
    )

    announcement_slug = announcements[0].slug
    announcement = (
        session.query(AnnouncementEntity)
        .filter(AnnouncementEntity.slug == announcement_slug)
        .one_or_none()
    )

    entities = []
    for comm in comments:
        entity = AnnouncementCommentEntity.from_model(comm)
        announcement.comments.append(entity)
        entities.append(entity)

    reset_table_id_seq(
        session,
        AnnouncementCommentEntity,
        AnnouncementCommentEntity.id,
        len(comments) + 1,
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
