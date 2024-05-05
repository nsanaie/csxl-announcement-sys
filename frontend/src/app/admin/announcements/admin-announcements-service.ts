import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { RxAnnouncement } from 'src/app/announcements/rx-announcements';
import { Announcement } from 'src/app/announcements/announcement.model';

@Injectable({ providedIn: 'root' })
export class AdminAnnouncementService {
  private announcements: RxAnnouncement = new RxAnnouncement();
  public announcements$: Observable<Announcement[]> = this.announcements.value$;

  constructor(protected http: HttpClient) {}

  /** Returns a list of all Announcements
   * @returns {Observable<Announcement[]>}
   */
  list(): void {
    this.http
      .get<Announcement[]>('/api/announcements/admin')
      .subscribe((announcements) => this.announcements.set(announcements));
  }

  /** Creates an announcement
   * @param newAnnouncement: Announcement object that you want to add to the database
   * @returns {Observable<Announcement>}
   */
  createAnnouncement(newAnnouncement: Announcement): Observable<Announcement> {
    return this.http
      .post<Announcement>('/api/announcements', newAnnouncement)
      .pipe(
        tap((announcement) => this.announcements.pushAnnouncement(announcement))
      );
  }

  /** Deletes an announcement
   * @param announcement_id: id of the announcement object to delete
   * @returns {Observable<Announcement>}
   */
  deleteAnnouncement(
    announcementToRemove: Announcement
  ): Observable<Announcement> {
    return this.http
      .delete<Announcement>(`/api/announcements/${announcementToRemove.slug}`)
      .pipe(
        tap((_) => {
          this.announcements.removeAnnouncement(announcementToRemove);
        })
      );
  }

  updateAnnouncement(announcementToUpdate: Announcement) {
    this.http
      .put<Announcement>(`/api/announcements/`, announcementToUpdate)
      .pipe(
        tap((announcement) => {
          this.announcements.updateAnnouncement(announcement);
        })
      )
      .subscribe();
  }

  // getAdminAnnouncement(announcement: Announcement) {
  //   this.http
  //     .get<Announcement>(`api/announcements/admin/` + announcement.slug)
  //     .pipe(
  //       tap((announcementToGet) => {
  //         this.announcements.getAdminAnnouncement(announcementToGet);
  //       })
  //     );
  // }
}
