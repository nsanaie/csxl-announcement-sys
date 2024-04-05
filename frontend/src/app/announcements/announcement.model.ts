/**
 * The Announcement Model defines the shape of Announcement data
 * retrieved from the Announcements Service and the API.
 *
 */

import { Organization } from '../organization/organization.model';

/** Enum for the state of the announcement */
export enum AnnouncementStatus {
  PUBLISHED = 'published',
  DRAFT = 'draft',
  ARCHIVED = 'archived'
}

/** Interface for Announcement Type (used on frontend for announcement detail) */
export interface Announcement {
  id: number | null;
  title: string;
  synopsis: string;
  body: string;
  organization: Organization | null;
  image?: string | null;
  state: AnnouncementStatus;
  viewCount: number | null;
  commentCount: number | null;
  shareCount: number | null;
  publishedDate: number | null;
  editedDate: number | null;
}
