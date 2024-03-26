# Team D4 XL News Feed and Announcement System
***Mark Maio, Nick Sanaie, Tanner Macpherson, Tyler Roth***

### Overview:
Within the CS department, there is not a central announcement system for students to pay attention to for getting involved in the department. The CSXL could help fill this void by providing an announcement system to be available for all CSXL users. The announcement system should convey CS department-wide events as well as providing personal announcements for users in different clubs.
 
### Key Personas:
1. Sally Student can view, share and comment on all public announcements on the CSXL website while logged into a student account.
2. Club Carl can create, edit, and delete can create public announcements about the club they lead.
3. Randy Random can view all public announcements on the CSXL website without being logged into an account.
4. Rhonda Root wants to be able to create, edit, and delete announcements.

### User Stories:
**Story A:** As Randy Random, I want to load up the CSXL website to see the latest news and announcements in an Announcements tab.\
**Story B:** As Sally Student, I want to be able to read public announcements, mark them as read or unread, share an announcement and comment on an announcement.\
**Story C:** As Club Carl, I want to be able to create public announcements for people to view information about my club/organization. I also want to be able to preview the announcement while creating it to see what it would look like when posted to the announcements page.\
**Story D:** As Club Carl, I want to edit or delete announcements I’ve created and see the statistics (views, comment count, likes). Additionally, the state of an announcement is one of the aspects that should be able to be edited (archived, draft, public).\
**Story E:** As Rhonda Root, I want to be able to create, edit, delete and observe the statistics of general announcements made by all User or Club admins.


### Wireframe:
[Link to Figma](https://www.figma.com/file/Jw80bpoSo5m65dmwR55eiH/COMP-590-Wireframes?type=design&node-id=0-1&mode=design&t=CdiZZleCVddNPrhE-0)

### Technical Implementation Opportunities and Planning:
**Dependencies**
- Users: Each announcement is associated with the user who created it. Their name is displayed with each announcement for accountability and communication.
- Roles: Rhonda Root can create, read, update, and delete announcements. Club Carl can create and read announcements, as well as update and delete their own announcements. Sally Student can read announcements and interact with them. Randy Random can only read announcements.
- Keep track of the user's level of access and functionality.

**Extensions**
- New database tables to store announcement-related data, such as the headline, synopsis, content, author, organization (optional), ID, and “read” or “unread”.

**Components and widgets**
- Announcement component: Side-nav route accessible for all user stories. Displays the announcements that have been made by other users
- Edit component: Interface for editing or deleting announcements that have been posted
- Announcement Preview widget: Displays title of announcement, which club it’s related to and details button
- Full Announcement widget: A larger widget for each announcement, displays the title, full text body, and the rest of the announcement details
- Creating announcement widget: Form for creating announcements
- Comment widget: Widget for each comment that a user makes, displayed with the announcement that it corresponds to

**Models**
- Announcement: Model used to store all the information necessary for an announcement. Encapsulates the subject object associated with the announcement, the full name of the user who created it, and the time and date of the event if provided
- Historical Announcements: Model used to store all announcements ever made. Encapsulates the Announcement model
-  Eligible Users: Model used to store a list of all students who are able to create announcements (Club Carls and Rhonda Roots). Encapsulates the User Models

**API / Routes**
- Get announcements (/announcements): Returns latest announcements in a scroll view. Intended purpose is to display all announcements. Used by all personas.
- Get announcement (/announcements/{slug_id}): Returns specific announcement. Intended purpose is to read more information about the announcement. Used by all personas.
- Post announcement (/announcements/edit/{slug_id}): Receives new announcements. Intended purpose is to update the announcement feed. Used by Club Carl and Rhonda Root.
- Put announcement data (/announcements/{slug_id}): Receives announcement update specifically for the user. Purpose is to mark an announcement as “read” or “unread” for the user. Used by Sally Student, Club Carl, and Rhonda Root.
- Delete announcement (/announcement/{slug_id}): Deletes an announcement. Intended purpose is to delete an announcement from the feed. Used by Club Carl and Rhonda Root. 
- Post comment (/announcements/{slug_id}/comments): Receives new comments under announcements. Purpose is to add new comments underneath an announcement. Used by Sally Student, Club Carl, and Rhonda Root.
- Delete comment (/announcements/{slug_id}/comments): Deletes comments under announcements. Purpose is to delete comments underneath an announcement. Used by Sally Student, Club Carl, and Rhonda Root, where Sally Student and Club Carl are only allowed to delete their own comments, while Rhonda Root can delete anyone’s comment.

**Security and privacy concerns**
- Rhonda Root is the only person who can edit/delete announcements aside from the creator of each announcement

