import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { AnnouncementsService } from './announcements.service';
import { Announcement } from './announcement.model';
import { AnnouncementStatus } from './announcement.model';

import { PermissionService } from '../permission.service';

import { catchError, map, switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

/** This resolver injects the list of announcement into the announcement component. */
export const announcementResolver: ResolveFn<Announcement[] | undefined> = (
  route,
  status
) => {
  return inject(AnnouncementsService).getAnnouncements();
};

export const announcementDetailResolver: ResolveFn<Announcement | undefined> = (
  route
) => {
  const slug = route.paramMap.get('slug');

  if (!slug || slug === 'new') {
    // If the slug is 'new' or undefined, return a new blank announcement
    return of({
      id: null,
      slug: '',
      headline: '',
      syn: '',
      body: '',
      image: '',
      status: AnnouncementStatus.DRAFT,
      organization_id: null,
      organization_slug: null,
      author_id: 0,
      view_count: 0,
      share_count: 0,
      upvote_count: 0,
      published_date: null,
      modified_date: null,
      archived_date: null,
      author: null,
      organization: null,
      comments: null
    });
  }

  // Inject PermissionService to check user permissions
  const permissionService = inject(PermissionService);
  let canViewAdmin: boolean = false;

  permissionService
    .check('announcement.view', 'announcement/')
    .subscribe((hasPermission) => {
      canViewAdmin = hasPermission;
    });

  return inject(AnnouncementsService)
    .getAnnouncement(slug!, canViewAdmin)
    .pipe(
      catchError((error) => {
        return of(undefined);
      })
    );
};
