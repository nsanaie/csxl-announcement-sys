/**
 * The Announcement Model defines the shape of Announcement data
 * retrieved from the Announcements Service and the API.
 *
 */

import { Organization } from '../organization/organization.model';
import { PublicProfile } from '../profile/profile.service';

/** Enum for the state of the announcement */
export enum AnnouncementStatus {
  PUBLISHED = 'published',
  DRAFT = 'draft',
  ARCHIVED = 'archived'
}

export enum AnnouncementSortMethod {
  NEWEST = 'newest',
  UPVOTES = 'upvotes',
  VIEWS = 'views'
}

export interface Comment {
  id: number;
  text: string;
  author_id: number;
  author: PublicProfile | null;
  posted_date: Date | null;
}

/** Interface for Announcement Type (used on frontend for announcement detail) */
// export interface Announcement {
//   id: number | null;
//   slug: string;
//   headline: string;
//   syn: string;
//   body: string;
//   image?: string | null;
//   status: AnnouncementStatus;
//   organization_id: number | null;
//   organization_slug: string | null;
//   author_id: number | null;
//   viewCount: number | null;
//   shareCount: number | null;
//   published_date: string | null;
//   edited_date: string | null;
//   archived_date: string | null;
//   author: PublicProfile | null;
//   organization: Organization | null;
//   comments: Comment[] | null;
// }

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

export interface UpvoteBoolean {
  upvoted: boolean;
}
