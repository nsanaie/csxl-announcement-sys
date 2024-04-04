/**
 * The Announcement Model defines the shape of Announcement data
 * retrieved from the Announcements Service and the API.
 *
 */

import { Organization } from '../organization/organization.model';

/** Interface for Announcement Type (used on frontend for announcement detail) */
export interface Announcement {
  id: number | null;
  title: string;
  synopsis: string;
  body: string;
  organization: Organization;
  viewCount: number | null;
  commentCount: number | null;
  shareCount: number | null;
  publishedDate: number;
  editedDate: number | null;
}
