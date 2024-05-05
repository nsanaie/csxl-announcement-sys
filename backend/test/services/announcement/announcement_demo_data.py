"""Contains mock data for the live demo of the organizations feature."""

import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ....models.announcement import Announcement, AnnouncementStatus
from ....models.announcement_comment import Comment
from ....entities.announcement_entity import AnnouncementEntity
from ....entities.announcements_comment_entity import AnnouncementCommentEntity

import time
import random

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

**Apply to join App Team Carolina on our [website](https://appteamcarolina.com/). Applications are due September 4, by 11:59 PM. If you have any questions or would like more information, feel free to reach out to me [here](nsanaie@ad.unc.edu.)**

Best, 

Nicholas Sanaie
App Team Carolina """,
    author_id=2,
    slug="appteamapps",
    organization_id=1,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/appteam.jpg",
    status=AnnouncementStatus.PUBLISHED,
    view_count=125,
    share_count=50,
    upvote_count=50,
)

announcement_2 = Announcement(
    id=2,
    headline="CS+SG Career Trek Applications Open!",
    syn="Computer Science + Social Good (CS+SG) is having a career trek at the Google headquarters in Durham on April 24th (tentatively) from 10am to 2pm!",
    body="""Hi all!
    
**I am happy to announce the CS+SG Career Trek!**

![](https://i.imgur.com/Aq8wuU3.png)
    
During this career trek, students will have the opportunity to network with employees at Google (including the Eastern regional recruiter!), learn about the culture at Google, and even get exclusive insight on Googles upcoming job and internship openings!! 
This opportunity is open to all students, and we encourage everyone to apply to attend before the application closes on April 12, 2024 at 11:59pm.
Food and transportation will be provided!

[Application Link](https://forms.gle/dhtysxEEzetSupjU6)

Questions or concerns? Email CS+SG at cssgunc@gmail.com.
    
Mark Maio""",
    author_id=1,
    slug="cssgtrek",
    organization_id=6,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cssg.png",
    status=AnnouncementStatus.PUBLISHED,
    view_count=150,
    share_count=35,
    upvote_count=48,
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

**We are excited to announce an upcoming Resume Workshop designed to help you craft the perfect resume and stand out in your job applications! Whether you're a student, a recent graduate, or a professional looking to take the next step in your career, this workshop is for you.**

### Workshop Details:

Date: 4/20/24
Time: 12:00pm
Location: Sitterson (or online if virtual)
RSVP: Please RSVP by Febuary 27th to secure your spot!

### What You Will Learn:

- How to tailor your resume for different job opportunities
- Tips for showcasing your skills and experiences effectively
- Strategies for using keywords to pass applicant tracking systems (ATS)
- Best practices for formatting and organizing your resume
- Real-life examples and templates to get you started

### What to Bring:

- A copy of your current resume (if you have one)
- A notebook and pen for taking notes

During the workshop, our expert facilitator will guide you through the process of creating a compelling resume that highlights your strengths and achievements. There will also be an opportunity for one-on-one feedback and Q&A sessions.

This workshop is a fantastic opportunity to enhance your resume and increase your chances of landing your dream job. We encourage you to join us for this informative and interactive session.

We look forward to seeing you at the workshop!

Best regards,
Tyler Roth""",
    author_id=1,
    slug="resume",
    organization_id=4,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
    status=AnnouncementStatus.PUBLISHED,
    view_count=225,
    share_count=100,
    upvote_count=75,
)

announcement_5 = Announcement(
    id=5,
    headline="UTA Applications are Open for Fall 2024",
    syn="UTA Applications are open for Fall '24 and due May 10th.",
    body="""Folks,

**UTA Applications are open for Fall '24 and due May 10th. We are moving away from an AirTable form submission to a custom web application form thanks to the work of Aziz Al-Shayef and Ben Goulet.**

### Applying is easy:

1. Login to the [CSXL](http://csxl.unc.edu/) via your ONYEN
2. After logging in, navigate to [Academics](https://csxl.unc.edu/academics)
3. Look for the Become a TA! pane and complete your application

As we transition to this new system, we ask all current UTAs applying to UTA again in the Fall to go ahead and submit this application. Please cite your current/former UTA experience in the question of "What experience do you have providing service directly to other people?" After this cycle, we will have a different form for returners; this is our bootstrapping semester.

One big, new feature of this application system is you can return to your application and edit it after you have submitted it.

Thanks!

Rhonda Root (Kris Jordan)  
Professor of the Practice  
Director of CS Experience Labs""",
    author_id=1,
    slug="uta-applications",
    status=AnnouncementStatus.PUBLISHED,
    view_count=550,
    share_count=225,
    upvote_count=180,
)

announcement_4 = Announcement(
    id=4,
    headline="Resume Workshop (February 28th)",
    syn="Resume workshop for aspiring SWEs, DS and PMs!",
    body="""Dear UNC students,

**We are excited to announce an upcoming Resume Workshop designed to help you craft the perfect resume and stand out in your job applications! Whether you're a student, a recent graduate, or a professional looking to take the next step in your career, this workshop is for you.**

### Workshop Details:

Date: 4/20/24
Time: 12:00pm
Location: Sitterson (or online if virtual)
RSVP: Please RSVP by Febuary 27th to secure your spot!

### What You Will Learn:

- How to tailor your resume for different job opportunities
- Tips for showcasing your skills and experiences effectively
- Strategies for using keywords to pass applicant tracking systems (ATS)
- Best practices for formatting and organizing your resume
- Real-life examples and templates to get you started

### What to Bring:

- A copy of your current resume (if you have one)
- A notebook and pen for taking notes

During the workshop, our expert facilitator will guide you through the process of creating a compelling resume that highlights your strengths and achievements. There will also be an opportunity for one-on-one feedback and Q&A sessions.

This workshop is a fantastic opportunity to enhance your resume and increase your chances of landing your dream job. We encourage you to join us for this informative and interactive session.

We look forward to seeing you at the workshop!

Best regards,
Tyler Roth""",
    author_id=1,
    slug="resume",
    organization_id=4,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
    status=AnnouncementStatus.PUBLISHED,
    view_count=225,
    share_count=100,
    upvote_count=75,
)

announcement_5 = Announcement(
    id=5,
    headline="UTA Applications are Open for Fall 2024",
    syn="UTA Applications are open for Fall '24 and due May 10th.",
    body="""Folks,

**UTA Applications are open for Fall '24 and due May 10th. We are moving away from an AirTable form submission to a custom web application form thanks to the work of Aziz Al-Shayef and Ben Goulet.**

### Applying is easy:

1. Login to the [CSXL](http://csxl.unc.edu/) via your ONYEN
2. After logging in, navigate to [Academics](https://csxl.unc.edu/academics)
3. Look for the Become a TA! pane and complete your application

As we transition to this new system, we ask all current UTAs applying to UTA again in the Fall to go ahead and submit this application. Please cite your current/former UTA experience in the question of "What experience do you have providing service directly to other people?" After this cycle, we will have a different form for returners; this is our bootstrapping semester.

One big, new feature of this application system is you can return to your application and edit it after you have submitted it.

Thanks!

Rhonda Root (Kris Jordan)  
Professor of the Practice  
Director of CS Experience Labs""",
    author_id=1,
    slug="uta-applications",
    status=AnnouncementStatus.PUBLISHED,
    view_count=550,
    share_count=225,
    upvote_count=180,
)

announcement_6 = Announcement(
    id=6,
    headline="Kappa Theta Pi Recruitment",
    syn="Get ready for Fall Recruitment!",
    body="""
    ## Hey everyone!

Kappa Theta Pi is holding its Fall Recruitment for this upcoming semester! Kappa Theta Pi, otherwise known as KTP, is a professional organization with an emphasis on technology!  
Fall recruitment dates for KTP are still TBD, but more information will come out soon. There is no specific major requirement - we are simply looking for students with a love for technology! KTP provides a great experience for anyone interested in growing professionally, socially, and academically. Through workshops, panels, and social events, members get the opportunity to develop professionally, learn new technical skills, and build a supportive network of students of UNC students and alumni with similar interests  
If you are someone who has a passion for technology and this interests you, be sure to register when the form comes out!  
Follow us on Instagram @ktpunc for all updates regarding Fall Recruitment! Click the link in our bio to view a Fall Recruitment FAQ to assist with answering questions. If you have any other questions, feel free to email me, Mark, at markmaio@ad.unc.edu.  
I hope you all have a great start to the semester!

Best,  
Mark Maio  
President of Kappa Theta Pi""",
    author_id=1,
    slug="ktp-rush",
    status=AnnouncementStatus.PUBLISHED,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/ktp.jpg",
    organization_id=13,
    view_count=320,
    share_count=104,
    upvote_count=104,
)

announcement_7 = Announcement(
    id=7,
    headline="AI @ UNC Announcements: Officer Applications, Kaggle",
    syn="AI @ UNC Applications for next school year!",
    body="""
# Hi everyone! Here are our weekly announcements!

- We are excited to announce that officer applications for the next school year are now open! We are looking for candidates for social chair, technical chair, treasurer, and more. The application deadline has been extended to May 10th. Please apply here (https://docs.google.com/forms/d/e/1FAIpQLSevACQafc7KlpUVInLKrus1-BwBvRnNrIMV2d7IKxgp2gm3Kg/viewform)!
- Also, our long term asynchronous Kaggle competition in collaboration with the UNC CS department’s Dr. Junier Oliva is still ongoing. Please refer to this link (https://www.kaggle.com/t/a0c74fd940494c519ef20583f505ec4b) for further details. The project involves data classification using a chemistry dataset, and you will have until LDOC to create your model. We will not be having drop-in office hours next week. 
- Additionally, the SLAE NLP project will be presented at the undergraduate research symposium on Monday, April 29th during Session 3 at 4:30 pm! Come check out Poster #143 in Alumni Hall at the Carolina Club (George Watt
s Hill Alumni Center) on Campus Drive.

**That's all for this week! As always, here is our feedback form](https://forms.gle/eLc8d4eQEQbj8mqt6)**

side note: *please make us an official org on the CSXL site!*

Thanks,  
Amy Ambassador  
Director of Communications: AI @ UNC""",
    author_id=2,
    slug="ai-unc-officer-apps",
    status=AnnouncementStatus.PUBLISHED,
    image="https://media.licdn.com/dms/image/D560BAQGUhfkHezKXqw/company-logo_200_200/0/1691374228289?e=1723075200&v=beta&t=KfZyEdJ44maBBD4a3CSO2j_Qk3KIv7sWzg58EPqXpnI",
    view_count=25,
    share_count=2,
    upvote_count=10,
)

announcement_8 = Announcement(
    id=8,
    headline="Unity Workshop",
    syn="Dive Deep into XR with Unity Workshop!",
    body="""
# Hey everyone!

This Thursday from **5:30 PM - 6:30 PM, join Carolina AR/VR in SN115** for a workshop that will continue introducing you to XR development within Unity. We will pick up from where we left off in our workshop on Thursday, March 7th (Dive into XR with Unity), and by the end of this workshop, you'll be able to build your own immersive experiences with a widely used game engine.

Mark your calendars, and if you have not done so, then read through and complete the pre-workshop setup beforehand! Please bring your laptop (with Unity and your XR assets already set up), and mouse to the workshop! Headsets are optional, as we will provide them.

If you have any questions regarding the pre-workshop setup, please join the Carolina AR/VR Discord server and ask in the Workshops channel!

We hope to see you there!

Best,
CARVR""",
    author_id=2,
    slug="unity",
    organization_id=5,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/arvr.png",
    status=AnnouncementStatus.PUBLISHED,
    view_count=41,
    share_count=12,
    upvote_count=20,
)

announcements = [
    announcement_6,
    announcement_1,
    announcement_2,
    announcement_3,
    announcement_4,
    announcement_5,
    announcement_7,
    announcement_8,
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
        if ann.status == AnnouncementStatus.PUBLISHED:
            current_date_time = datetime.now()
            last_month_end = current_date_time.replace(day=1) - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            num_days_in_last_month = (last_month_end - last_month_start).days + 1
            random_days_ago = random.randint(0, num_days_in_last_month - 1)
            random_date = last_month_end - timedelta(days=random_days_ago)
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            random_datetime = random_date.replace(
                hour=random_hour, minute=random_minute
            )
            ann.published_date = random_datetime
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
