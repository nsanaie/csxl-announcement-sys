## Technical Specification

1.

```
export interface Announcement {
  id: number | null;
  slug: string | null;
  title: string;
  synopsis: string;
  body: string;
  organization: Organization | null;
  image?: string | null;
  state: AnnouncementStatus;
  viewCount: number | null;
  commentCount: number | null;
  shareCount: number | null;
  publishedDate: Date | null;
  editedDate: Date | null;
}
```

```
export interface Comment {
  id: number;
  text: string;
  author_id: number;
  author: PublicProfile | null;
  posted_date: string;
}
```

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
)
```

```
comment_2 = Comment {
  id: 2;
  text: "Can't wait to attend";
  author_id: 1;
  author: "Sally Student";
  posted_date: "04/17/2024";
}
```

These are sample announcements and comments that are loaded into the backend of our project

API Routes:
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

For StoryA, we want to be able to retrieve announcements by their slug to view their information

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

    For StoryB, we want to be able to create comments and share the announcement link

2.

- We created an AnnouncementEntity that mirrors the backend announcement model. The id is a number and is the primary key
- An AnnouncementEntity will have a one-many relationship with authors, as one author can have many announcements but an announcement can only be assigned to a single author
- There is a one-to-many relationship between organizations and announcements
- There is a one-to-many relationship between announcements and comments as well
- We also created a CommentEntity
- There is a one-to-many relationship between authors and comments
- There is a one-to-many relationship between announcements and comments

3.

Technical:

- In the frontend announcement service, we chose to use a resolver class to be able to load the corresponding data for each announcement from the backend. On the contrary, we could have stored all of the announcements from the backend in the frontend service and gotten the corresponding announcement from the array of announcements. This decision allows for quicker load times for the user as the frontend wouldn't need to use as much memory in storing all announcements- it would just need to retrieve one announcement by slug from the backend.

User Experience:

-
