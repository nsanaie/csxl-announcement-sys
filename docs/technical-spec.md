# Team D4 XL News Feed and Announcement System

**_Mark Maio: https://github.com/markmaio_**

**_Nick Sanaie: https://github.com/nsanaie_** 

**_Tanner Macpherson: https://github.com/TannerM03_**
 
**_Tyler Roth: https://github.com/tylertho_**

### Overview:

Within the CS department, there is not a central announcement system for students to pay attention to for getting involved in the department. The CSXL could help fill this void by providing an announcement system to be available for all CSXL users. The announcement system should convey CS department-wide events as well as providing personal announcements for users in different clubs

### Key Personas:

1. Sally Student can view, share and comment on all public announcements on the CSXL website while logged into a student account.
2. Randy Random can view all public announcements on the CSXL website without being logged into an account.
3. Rhonda Root wants to be able to create, edit, and delete announcements.

## Technical Specification

### Models

Several new models were introduced within this feature. Firstly and most importantly, the announcement model was created in the frontend to store information relating to all individual announcements. As seen below, announcement objects are identified by a unique id and slug. Announcements also have a headline, synopsis, body. Announcements also have optional fields of organization and image. When published, an announcement uses the provided image as the image for the announcement. If no image is provided, the announcement uses the default image for the organization the announcement is associated with. If there is no organization associated with the announcement, the announcement uses the github avatar of the author or generates an avatar for the author if they don't have one. All announcements also included a status variable which is defined below; all announcements can either be published, drafted, or archived. Each of these states played a vital role in authorization for different users and roles being able to view certain announcements. These permissions will be elaborated later in the document. Along with these fields already listed, each respective announcement also contains fields for view count, comment count, and share count. These fields can be optional for announcements that are still in a draft state and won't have these fields be altered in any way. Along the same lines, the published date and edited date fields will be set when an announcement is published, but are initialized to null for when an announcement is in a draft state.

```
export interface Announcement {
  id: number | null;
  slug: string;
  headline: string;
  syn: string;
  body: string;
  image: string | null;
  status: AnnouncementStatus;
  organization_id: number | null;
  organization_slug: string | null;
  author_id: number | null;
  view_count: number | null;
  share_count: number | null;
  upvote_count: number | null;
  published_date: Date | null;
  modified_date: Date | null;
  archived_date: Date | null;
  author: PublicProfile | null;
  organization: Organization | null;
  comments: Comment[] | null;
}

export enum AnnouncementStatus {
  PUBLISHED = 'published',
  DRAFT = 'draft',
  ARCHIVED = 'archived'
}
```

To represent announcements in the backend, the following object structure was used. The main difference in this model in the backend is every announcement has a unique author. Having this author field allowed for authorization performing CRUD operation. For example, in the Randy Random persona, only published announcements should be available to them. As Rhonda Root, announcements in published, drafted, and archived states can be viewed given various circumstances.

```
class Announcement(BaseModel):
    """
    Pydantic model to represent an `Announcement`.
    """

    id: int | None = None
    headline: str
    syn: str
    body: str
    author_id: int
    author: PublicUser | None = None
    slug: str
    organization_id: int | None = None
    organization_slug: str | None = None
    image: str | None = None
    status: AnnouncementStatus
    published_date: datetime | None = None
    modified_date: datetime | None = None
    archived_date: datetime | None = None
    view_count: int = 0
    share_count: int = 0
    upvote_count: int = 0

class AnnouncementStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
```

Below is an example of an announcement created to act as dummy data in the backend to be loaded when the database is initially created. The backend entity handles the addition of posted, modified and archived dates and the association between author_id and its respective entity.

```
announcement_3 = Announcement(
    id=3,
    headline="CSSG interest meeting",
    syn="Positions open for project and education members",
    body="Positions open for project and education members. Apply for CSSG by Feb 9 to work on one of our project teams.",
    author_id=1,
    slug="pminterestdraft",
    organization_id=6,
    image="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pm.jpg",
    status=AnnouncementStatus.DRAFT,
    view_count=0,
    share_count=0,
    upvote_count=0
)
```

Additionally, a model is provided in the backend for modeling the additional details of an individual announcement. The `AnnouncementDetails` object encapsualtes an `Announcement` object and contains the organization and list of comments associated to a specific announcement. Similar to author_id, the organization model is retrived using the organization entity associated with the announcement's organization_id. Commenting functionality is elaborated on further below. This object is what is returned to the frontend when we want to view the details page of a specific announcement instead of just the preview.

```
class AnnouncementDetails(Announcement):
    """
    Pydantic model to represent the details of an `Announcement`.
    """

    organization: Organization | None = None
    comments: list[Comment] = []
```

With each announcement, there is the ability for authorized users to make comments. Every comment posted by a user will only correspond to one announcement. In the frontend, comments are modeled as below. Each comment is uniquely identified by an id. They also contain the author which is represented by a ```PublicProfile``` object which represents the additional author data for additional information such as author name required in the frontend.

```
export interface Comment {
  id: number;
  text: string;
  author_id: number;
  author: PublicProfile | null;
  posted_date: string;
}
```

In the backend, comments are modeled similarly. The only difference being author being represented by a ```PublicUser``` object which closely mirrors the ```PublicProfile``` object being used in the frontend. 

```
class Comment(BaseModel):
    """
    Pydantic model to represent a comment on an announcement.
    """

    id: int
    text: str
    author_id: int
    author: PublicUser | None = None
    posted_date: str
```

An example of a comment created to act as dummy data. The posted date and author model is created automatically in the backend services using the current date and the author id respectively.

```
comment_2 = Comment {
  id: 2;
  text: "Can't wait to attend";
  author_id: 1;
}
```

To enable users to upvote individual announcements, a model is provided under the frontend announcement model. The interface is employed to make sure users can only upvote, unvote, favorite and unfavorite an announcement **once.**- ensuring liking a post can't be done more than once by a single user. The `upvoted` field will tell the application the status of the user for that given statistic (if they have upvoted or favorited an announcement etc)

```
export interface UpvoteBoolean {
  upvoted: boolean;
}
```

In the backend, this model was created to mirror the frontend ```UpvoteBoolean``` model.

```
class UpvoteBoolean(BaseModel):
    upvoted: bool
```

### Components
The main component added was the announcements component added into the app directory in the frontend. Within this component, there is an announcement resolver used extensively in displaying information for announcement details. These is also the routing module used for routing within the component and elsewhere on the website, the announcements module for storing the widgets and other dependencies, a RxJS announcement class for notifying other classes when announcements are changed through CRUD operations, and an announcement service used in calling API endpoints.

In the announcements component, there are three other components: announcements-editor, announcement-details, and announcements-page. The announcement-editor component is used when an authorized user tries to create or edit an announcement. The user is brought to a page with a form with fields matching the announcement object when they can insert and change information. The announcement-details component is used when any user clicks the details button on an announcement card. This routes a user to a page where the announcement details page widget is displayed along with all comments for that announcement being displayed below it. The announcement-page component is used when a user clicks on the announcements tab in the navigation bar. This routes a user to a page where all announcements are displayed using announcement card widgets.

Outside of the main announcements component, an announcement folder was added to the admin component. Within this folder, an admin announcements list component was created. This allows for admin users to have a tab under the admin page for viewing all announcements visible to that respective admin user- all published announcements, archived announcements created by admin user, and drafted announcements created by admin user(this will be elaborated on later in the document).

***Note: Why Anglular 17?***
***NGX/Markdown wasn’t supported well by Angular 15. Angular 17 better supports markdowns for text input. Angular 17 also provided dependency injection debugging tools vital for editing and creating announcements in this feature's case.***

### Widgets

Two widgets were created in the frontend: ```announcement-card-widget``` and ```announcement-details-page-widget```. 

The announcement card widget is used on the announcement page to display respective information for every announcement posted such as announcement image, title, synopsis, and buttons for clicking on the announcement details and corresponding organization. 

The announcement details page widget is used when a user clicks on the details button on an announcement card. This routes the user to the announcement details page where the announcement details widget is used. This is displayed above where comments are displayed. The entirety of the information for an announcement is displayed such as the body, published date, comments, like count, and buttons for sharing, favoriting, commenting, and liking.

### Frontend Services

Two frontend services were created: ```announcement-service``` and ```admin-announcement-service```. The announcement-service provides functions for the frontend in calling the API endpoints for CRUD methods being performed on different objects- ```Announcement``` and ```Comment```. It also provides functions for changing values of upvote counts, view counts, share counts, and sorting methods used in the announcement page.

The admin-announcement-service provides functions used when admin users are under the admin/announcements tab. These include create, delete, and update functions as this is the page where admin users will be able to have complete functionality/command over announcements that they're authorized to view.

On the announcement page where all announcements are displayed, there are different filter options for users to select announcements to view based on these options. ###FILL IN

```
export enum AnnouncementSortMethod {
  NEWEST = 'newest',
  UPVOTES = 'upvotes',
  VIEWS = 'views'
}
```

### API Endpoints

Transitioning to the backend, one new API was created- the announcements API. Within this API, many API endpoints were created for operations regarding announcements. There are endpoints that use the same HTTP methods, but correspond to different users being able to call them- mainly as a result in the difference between announcement-service and admin-announcement-service. 

#### Get
```get_published_announcements```, ```get_admin_announcements```, ```get_announcement```, ```get_admin_announcement```, ```check_user_favorite```, and ```check_user_upvote```. 

- ```get_published_announcements```: called in the announcements page component. This endpoint can be used by all users as all users should be able to view all published announcements.
- ```get_admin_announcements```: called in the admin/announcements page where all announcements are displayed that the admin user has authorization to view. Reasoning for announcement viewing authorization is provided in a note below. 
- ```get_announcement```: called in the announcements details page and called by any user to access a specific announcement that they have access to. This can be used by all users regardless of their authentication level.
- ```get_admin_announcement```: similar to get_announcement as there is no button or direct call to the endpoint- can only be called by a user directly entering the URL.
- ```check_user_favorite```: called from announcements details page when user clicks favorite button to check if the user has favorited the given announcement already.
- ```check_user_upvote```: called from announcements details page when user clicks upvote button to check if the user has upvoted the given announcement already.

***NOTE: Admin users are designed to only be able to view all published announcements, all archived announcements in which they created, and all draft announcements in which they created. As an admin, the creators of this feature believed an admin should have authorization and command over all published announcements, regardless of user, as the user willingly published that announcement. For archived announcements, if a user decided to archive an announcement, one could assume that that announcement was out-of-date or that the author doesn't want that announcement to be viewed by anyone but themselves any longer. So in order to respect the privacy of the user, the admin should not be able to view archived announcements that aren't created by that admin user. Along the same lines for draft announcements, if a user decides to save an announcement as a draft, they aren't ready for the announcement to be viewed by all users. Again, in aims of preserving privacy, admin users should only be able to view draft announcements created by themselves.***

#### Put
```update_announcement```, ```increment_views```, ```increment_shares```, ```favorite```, ```unfavorite```, ```increment_upvotes```, and ```decrement_upvotes```. 
- ```update_announcement```: called by admin users when they are editing a published, archived, or drafted announcement. Specifically, by the save button on the announcement-editor form when the announcement had already been initialized in one of the three states. 
- ```increment_views```: called when a user clicks on the details button of an announcement card.
- ```increment_shares```: called when a user clicks the share button within the announcements details page.
- ```favorite```: called when a user clicks the favorite icon on the announcements details page.
- ```unfavorite```: called when a user has already favorited an announcement and wants to unfavorite an announcement.
- ```increment_upvotes```: called when a user clicks on the upvote button on the announcements details page.
- ```decrement_upvotes```: called when a user has already upvoted an announcement and wants to remove there upvote from the announcement.

#### Post
```new_announcement``` and ```new_comment```. 
- ```new_announcement```: called when an authorized user is creating an announcement and presses the save button on the announcement editor form- intending to publish the announcement. Also called when a user presses the save to draft button in the announcement editor intending to create the announcement but just save it as a draft.
- ```new_comment```: sequentially called when a user clicks on the comments button on the announcements details page. An input box appears and once they press enter for their comment to be posted, API call is made.

#### Delete
```delete_announcement```. 
- ```delete_announcement``` is called when an admin user is under the admin announcements tab and clicks the delete button on an individual announcement card.

### Backend Services
One backend service was created, ```AnnouncementService```. This service provides all methods for performing CRUD operations corresponding to API calls.

#### Get Service Methods
```all_published```, ```all_admin```, ```get_by_slug```, ```get_by_slug_admin```, ```check_upvote```, and ```check_favorite```
- ```all_published```: returns all announcements that are published. 
- ```all_admin```: returns all announcements that are of published, archived with same author id, and drafted with same author id. Permissions are checked for only admin users to be able to access method.
- ```get_by_slug```: returns announcement details of announcement matching slug queried. Throws ```ResourceNotFoundException``` if announcement doesn't exist or if user doesn't have permission to access announcement.
- ```get_by_slug_admin```: returns announcement details of announcement matching slug queried. Throws ```ResourceNotFoundException``` if announcement doesn't exist or if admin user doesn't have permission to access announcement.
- ```check_upvote```: returns announcement that user is trying to upvote. User passed in as argument to query for ```UserEntity``` with matching user id. Slug passed in as argument to query for ```AnnouncementEntity``` with matching slug. Throws ```ResourceNotFoundException``` if announcement doesn't exist.
- ```check_favorite```: returns announcement that user is trying to favorite. User passed in as argument to query for ```UserEntity``` with matching user id. Slug passed in as argument to query for ```AnnouncementEntity``` with matching slug. Throws ```ResourceNotFoundException``` if announcement doesn't exist.

#### Put Service Methods
```update_announcement```, ```update_views```, ```update_shares```, ```add_favorite```, ```remove_favorite```, ```add_upvote```, and ```remove_upvote```.
- ```update_announcement```: returns announcement with updated information. User passed in as argument to query for ```UserEntity``` with matching author id in order to ensure authorization. Announcement passed in as argument to query for ```AnnouncementEntity``` with matching slug and ```OrganizationEntity``` based off of organization_id from announcement argument. Throws ```ResourceNotFoundException``` if author doesn't exist in database, if organization entity doesn't exist in database, or if announcement entity doesn't exist in database. Functionality provided for replacing image field of returned announcement if the announcement argument doesn't already have a value for image field. Additionally, functionality provided for updating modified_date and archived_date fields based on current state of announcement argument when passed in. Sets rest of fields of announcement entity to the field value of announcement argument.
- ```update_views```: returns announcement with incremented view_count field. Throws ```ResourceNotFoundException``` if no announcement found with matching slug argument.
- ```update_shares```: returns announcement with incremented share_count field. Throws ```ResourceNotFoundException``` if no announcement found with matching slug argument.
- ```add_favorite```: returns announcement that is being favorited. Slug passed in as argument to query for ```AnnouncementEntity``` with matching slug. User passed in as argument to query for ```UserEntity``` with matching id of User argument. Throws ```ResourceNotFoundException``` if no announcement found with matching slug argument. Checks if queried announcement entity is already in the user's list of favorites. If _false_, announcement entity is added to list of subject's favorites.
- ```remove_favorite```: returns announcement that is being favorited. Slug passed in as argument to query for ```AnnouncementEntity``` with matching slug. User passed in as argument to query for ```UserEntity``` with matching id of User argument. Throws ```ResourceNotFoundException``` if no announcement found with matching slug argument. Checks if queried announcement entity is already in the user's list of favorites. If _true_, announcement entity is added to list of subject's favorites.
- ```add_upvote```: returns announcement user is trying to upvote. User passed in as argument to query for ```UserEntity``` with matching user id. Slug passed in as argument to query for ```AnnouncementEntity``` with matching slug. Throws ```ResourceNotFoundException``` if announcement doesn't exist. Checks if calling ```upvote_announcement``` on queried user entity with queried announcement entity returns true. If so, announcement entity upvote_count incremented.
- ```remove_upvote```: returns announcement user is trying to un-upvote. User passed in as argument to query for ```UserEntity``` with matching user id. Slug passed in as argument to query for ```AnnouncementEntity``` with matching slug. Throws ```ResourceNotFoundException``` if announcement doesn't exist. Checks if calling ```remove_announcement``` on queried user entity with queried announcement entity returns true. If so, announcement entity upvote_count decremented.

#### Post Service Methods
```create``` and ```create_comment```.
- ```create```: returns announcement created from method. User passed in as argument to query for ```UserEntity``` with matching author id in order to ensure authorization. Announcement passed in as argument to query for ```AnnouncementEntity``` with matching slug and ```OrganizationEntity``` based off of organization_id from announcement argument. Throws ```ResourceNotFoundException``` if author doesn't exist in database, if organization entity doesn't exist in database, or if there already exists an announcement with a slug being used to create new announcement. Functionality provided for replacing image field of announcement if the announcement argument doesn't already have a value for image field. Announcement entity created then added to database.
- ```create_comment```: returns comment created from method. User passed in as argument to query for ```UserEntity``` with matching author id in order to ensure authorization.  Slug (string) passed in as argument to query for ```AnnouncementEntity``` with matching slug. Throws ```ResourceNotFoundException``` if no announcement is found. Checks that comment author id matches the user id trying to create the comment. Comment entity created then added to database.

#### Delete Service Methods
```delete```.
- ```delete```: returns nothing. User passed in as argument to ensure authorization. Slug passed in as argument to query for ```AnnouncementEntity``` with matching slug. Throws ```ResourceNotFoundException``` if no announcement found with matching slug. Announcement entity queried then deleted from database.

### Entities

Two entities were created: ```AnnouncementEntity``` and ```AnnouncementCommentEntity```, and two relationship tables: ```announcement_upvote_table``` and ```announcement_favorite_table```. ```UserEntity``` was edited.

#### ```AnnouncementEntity```
Fields:
- id: Unique identifier for the announcement. (Type: Integer)
- headline: Headline/title of the announcement. (Type: String)
- syn: Synopsis/summary of the announcement. (Type: String)
- body: Detailed body content of the announcement. (Type: String)
- slug: Unique slug for the announcement. (Type: String)
- image_url: URL of the image associated with the announcement. (Type: String)
- status: Status of the announcement (e.g., Draft, Published). (Type: Enum)
- view_count: Number of times the announcement has been viewed. (Type: Integer)
- share_count: Number of times the announcement has been shared. (Type: Integer)
- upvote_count: Number of upvotes received for the announcement. (Type: Integer)
- published_date: Date and time when the announcement was published. (Type: DateTime)
- modified_date: Date and time when the announcement was last modified. (Type: DateTime)
- archived_date: Date and time when the announcement was archived. (Type: DateTime)
- author_id: Foreign key reference to the author of the announcement. (Type: Integer)
- organization_id: Foreign key reference to the organization associated with the announcement. (Type: Integer)

Relationships:
- author: One-to-many relationship with the ```UserEntity``` class representing the author of the announcement.
- organization: One-to-many relationship with the ```OrganizationEntity``` class representing the organization associated with the announcement.
- comments: One-to-many relationship with the ```AnnouncementCommentEntity``` class representing comments associated with the announcement.
- upvotes: Many-to-many relationship with the ```UserEntity``` class representing users who have upvoted the announcement. Uses ```announcement_upvote_table``` relation table described below.
- favorites: Many-to-many relationship with the ```UserEntity``` class representing users who have marked the announcement as a favorite. Uses ```announcement_favorite_table``` relation table described below.

Class methods:
- from_model: Converts an instance of the ```Announcement``` into an ```AnnouncementEntity```.
- to_model: Converts an ```AnnouncementEntity``` into an instance of the ```Announcement```.
- to_details_model: Converts an ```AnnouncementEntity``` into an instance of the ```AnnouncementDetails```.

#### ```AnnouncementCommentEntity```
Fields: 
- id: Unique identifier for the comment. (Type: Integer)
- text: Text content of the comment. (Type: String)
- posted_date: Date when the comment was posted. (Type: String)
- author_id: Foreign key reference to the author of the comment. (Type: Integer)
- announcement_id: Foreign key reference to the announcement associated with the comment. (Type: Integer)

Relationships:
- author: One-to-many relationship with the ```UserEntity``` class representing the author of the comment.
- announcement: One-to-many relationship with the ```AnnouncementEntity``` class representing the announcement associated with the comment.

Class methods:
- from_model: Converts an instance of the ```Comment``` model into an ```AnnouncementCommentEntity```.
- to_model: Converts an ```AnnouncementCommentEntity``` into an instance of the ```Comment``` model.

#### ```announcement_upvote_table```
Users can upvote many announcements and announcements can have many upvotes from different users. Matches announcement id with user id.

#### ```announcement_favorite_table```
Users can favorite many announcements and announcements can have many favorites from different users. Matches announcement id with user id.

#### ```UserEntity``` changes
Fields (added):
- announcements: One-to-many relationship with the ```UserEntity``` class representing the author of the announcement.
- announcement_comments: One-to-many relationship with the ```AnnouncementEntity``` class representing the announcement associated with the comments.
- announcement_upvotes: Many-to-many relationship with the ```UserEntity``` class representing users who have upvoted the announcement. Uses ```announcement_upvote_table``` relation table described below.
- announcement_favorites: Many-to-many relationship with the ```UserEntity``` class representing users who have marked the announcement as a favorite. Uses ```announcement_favorite_table``` relation table described below.

Methods (added):
- ```upvote_announcement```: returns void. Check if announcement_entity argument not in the user's list of announcement_upvotes already. If true, announcement entity is added to user's list of upvoted announcements.
- ```remove_upvote_announcement```: returns void. Check if announcement_entity argument is in the user's list of announcement_upvotes already. If true, announcement entity is removed from user's list of upvoted announcements.
- ```check_upvote_announcement```: returns boolean from result of checking to see if announcement entity argument is in user's list of upvoted announcements.


### Testing

#### AnnouncementService
- ```all_published```: Ensured all personas can get and view all published announcements.
- ```all_admin```: Ensured admin can get and view all published announcements, get and view all archived announcements where they were the author, and get and view all drafted announcements where they were the author. Ensured admin can't get and view all and archived drafted announcements where they weren't the author.
- ```get_by_slug```: Ensured all personas can get and view a published announcement by giving a slug of an published announcement. Asserted an announcement wasn't found when given a nonexistent slug. Ensured user can't view an announcement that wasn't published.
- ```get_by_slug_admin```: Ensured admin user can get and view a published announcement by giving a slug of a published announcement, archived announcement with corresponding author id, or draft announcement with corresponding author id. Asserted an announcement wasn't found when given a nonexistent slug. Ensured admin user can't view an announcement that was archived and drafted with different author id then admin user.

- ```update_announcement```: Ensured an admin user can update an already existing announcement given an existent slug. Asserted updated fields of an announcement are equal to fields of announcement argument passed in with corresponding slug. Confirmed announcement couldn't be updated when given announcement with nonexistent slug. Ensured announcement couldn't be updated given nonexistent announcement id. Made sure announcement couldn't be updated given nonexistent organization id.
- ```update_views```: Ensured an announcement's view_count field is incremented by one after method call. Asserted a user can't increment the view_count of an announcement twice. Confirmed an exception is thrown given a nonexistent slug.
- ```update_shares```: Ensured an announcement's share_count field is incremented by one after method call. Asserted a user can't increment the share_count of an announcement twice. Confirmed an exception is thrown given a nonexistent slug.
- ```add_favorite```: Ensured a user's announcement_favorites has the newly favorited announcement in the list. Confirmed an exception is thrown given a nonexistent slug.
- ```remove_favorite```: Ensured a user's announcement_favorites doesn't have the newly removed favorited announcement in the list. Confirmed an exception is thrown given a nonexistent slug.
- ```add_upvote```: Ensured a user's announcement_upvotes has the newly upvoted announcement in the list. Asserted a user's announcement_upvotes list is incremented by one. Confirmed an exception is thrown given a nonexistent slug.
- ```remove_upvote```: Ensured a user's announcement_upvotes doesn't have the newly un-upvoted announcement in the list. Asserted a user's announcement_upvotes list is decremented by one. Confirmed an exception is thrown given a nonexistent slug.

- ```create```: Ensured admin user can create several announcements in published and draft states. Asserted any user can't create an announcement where the slug already exists. Confirmed create would fail when given invalid parameters for creating an announcement.
- ```create_comment```: Ensured authorized users (Sally Student and Rhonda Root) can create comments under individual announcements. Confirmed unauthorized users (Randy Random) can not create comments. Asserted comments can't be create where the author id of the comment doesn't match the user id.

- ```delete```: Ensured that only admin users can delete announcements. Asserted that announcement can't be retrieved after being deleted. Confirmed announcement can't be deleted given a nonexistent slug.