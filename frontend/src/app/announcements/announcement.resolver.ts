import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { AnnouncementsService } from './announcements.service';
import { Announcement } from './announcement.model';
import { AnnouncementStatus } from './announcement.model';

import { catchError, map, of } from 'rxjs';

/** This resolver injects the list of announcement into the announcement component. */
export const announcementResolver: ResolveFn<Announcement[] | undefined> = (
  route,
  state
) => {
  return inject(AnnouncementsService).getAnnouncements();
};

/** This resolver injects an announcement into the announcement detail component. */
export const announcementDetailResolver: ResolveFn<Announcement | undefined> = (
  route,
  state
) => {
  // Otherwise, return the announcement.
  // If there is an error, return undefined
  return inject(AnnouncementsService)
    .getAnnouncement(route.paramMap.get('slug')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};
