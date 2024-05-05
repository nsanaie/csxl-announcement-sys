import { Injectable } from '@angular/core';
import {
  Announcement,
  UpvoteBoolean,
  AnnouncementSortMethod
} from './announcement.model';
import { Comment } from './announcement.model';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class AnnouncementsService {
  private sortMethod: AnnouncementSortMethod;
  private currentPage: number;
  private isFavoriteOn: boolean;

  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {
    this.sortMethod = AnnouncementSortMethod.NEWEST;
    this.currentPage = 1;
    this.isFavoriteOn = false;
  }

  getCurrentPage(): number {
    return this.currentPage;
  }

  setCurrentPage(newPage: number): number {
    this.currentPage = newPage;
    return this.currentPage;
  }

  getFavoriteToggle(): boolean {
    return this.isFavoriteOn;
  }

  setFavoriteToggle(setting: boolean): boolean {
    this.isFavoriteOn = setting;
    return this.isFavoriteOn;
  }

  getSortMethod(): AnnouncementSortMethod {
    return this.sortMethod;
  }

  setSortMethod(newSortMethod: AnnouncementSortMethod): AnnouncementSortMethod {
    this.sortMethod = newSortMethod;
    return this.sortMethod;
  }

  /** Returns all announcement entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Announcement[]>}
   */
  getAnnouncements(): Observable<Announcement[]> {
    return this.http.get<Announcement[]>('/api/announcements');
  }

  /** Returns the announcement object from the backend database table using the backend HTTP get request.
   * @param slug: String representing the announcement slug
   * @returns {Observable<Annoucement>}
   */
  getAnnouncement(slug: string, perm: boolean): Observable<Announcement> {
    if (perm) {
      return this.http.get<Announcement>(`api/announcements/admin/` + slug);
    } else {
      return this.http.get<Announcement>('/api/announcements/' + slug);
    }
  }

  getAdminAnnouncement(slug: string): Observable<Announcement> {
    return this.http.get<Announcement>(`api/announcements/admin/` + slug);
  }

  createAnnouncement(announcement: Announcement): Observable<Announcement> {
    return this.http.post<Announcement>('/api/announcements', announcement);
  }

  updateAnnouncement(announcement: Announcement): Observable<Announcement> {
    return this.http.put<Announcement>('/api/announcements/', announcement);
  }

  updateShareCount(slug: string): Observable<Announcement> {
    return this.http.put<Announcement>(
      '/api/announcements/' + slug + '/shareCount',
      null
    );
  }

  updateViewCount(slug: string): Observable<Announcement> {
    return this.http.put<Announcement>(
      '/api/announcements/' + slug + '/viewCount',
      null
    );
  }

  addUserFavorite(slug: string): Observable<UpvoteBoolean> {
    return this.http.put<UpvoteBoolean>(
      '/api/announcements/' + slug + '/addFavorite',
      null
    );
  }

  removeUserFavorite(slug: string): Observable<UpvoteBoolean> {
    return this.http.put<UpvoteBoolean>(
      '/api/announcements/' + slug + '/removeFavorite',
      null
    );
  }

  checkUserFavorite(slug: string): Observable<UpvoteBoolean> {
    return this.http.get<UpvoteBoolean>(
      '/api/announcements/' + slug + '/checkFavorite'
    );
  }

  incrementUpvoteCount(slug: string): Observable<UpvoteBoolean> {
    return this.http.put<UpvoteBoolean>(
      '/api/announcements/' + slug + '/addUpvote',
      null
    );
  }

  decrementUpvoteCount(slug: string): Observable<UpvoteBoolean> {
    return this.http.put<UpvoteBoolean>(
      '/api/announcements/' + slug + '/removeUpvote',
      null
    );
  }

  checkUserUpvote(slug: string): Observable<UpvoteBoolean> {
    return this.http.get<UpvoteBoolean>(
      '/api/announcements/' + slug + '/checkUpvote'
    );
  }

  createComment(comment: Comment, slug: string): Observable<Comment> {
    return this.http.post<Comment>(
      'api/announcements/' + slug + '/comments',
      comment
    );
  }
}
