import { Injectable } from '@angular/core';
import { Organization } from '../organization/organization.model';
import { Announcement } from './announcement.model';
import { Comment } from './announcement.model';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class AnnouncementsService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

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
  getAnnouncement(slug: string): Observable<Announcement> {
    return this.http.get<Announcement>('/api/announcements/' + slug);
  }

  updateShareCount(slug: string): Observable<Announcement> {
    return this.http.put<Announcement>(
      '/api/announcements/' + slug + '/shareCount',
      null
    );
  }

  updateViewCount(slug: String): Observable<Announcement> {
    return this.http.put<Announcement>(
      '/api/announcements/' + slug + '/viewCount',
      null
    );
  }

  createComment(comment: Comment, slug: string): Observable<Comment> {
    return this.http.post<Comment>(
      'api/announcements/' + slug + '/comments',
      comment
    );
  }
}
