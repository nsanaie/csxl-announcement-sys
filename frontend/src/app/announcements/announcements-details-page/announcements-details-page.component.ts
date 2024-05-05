import { Component, OnInit } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route,
  Router
} from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, BehaviorSubject } from 'rxjs';
import { Announcement } from '../announcement.model';
import { AnnouncementsService } from '../announcements.service';
import { AnnouncementStatus } from '../announcement.model';
import { announcementDetailResolver } from '../announcement.resolver';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { PermissionService } from 'src/app/permission.service';
import { AnnouncementDetailsPageWidgetComponent } from '../widgets/announcement-details-page-widget/announcement-details-page-widget.component';
import { Profile } from 'src/app/models.module';
import { Comment } from '../announcement.model';
import { AuthenticationService } from 'src/app/authentication.service';

// /** Injects the announcement's name to adjust the title. */
// let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
//   return route.parent!.data['announcement']?.name ?? 'Announcement Not Found';
// };

@Component({
  selector: 'app-announcements-details-page',
  templateUrl: './announcements-details-page.component.html',
  styleUrls: ['./announcements-details-page.component.css']
})
export class AnnouncementsDetailsPageComponent implements OnInit {
  id: number = 0;
  userComment: string = '';
  comments: Comment[] = [];
  author: string = '';
  slug: string = '';

  addLeadingZero(num: number): string {
    return num < 10 ? `0${num}` : `${num}`;
  }

  public static Route = {
    path: ':slug',
    component: AnnouncementsDetailsPageComponent,
    resolve: {
      announcement: announcementDetailResolver,
      profile: profileResolver
    }
  };
  displayedComment: string = '';

  public announcement: Announcement;
  public profile: Profile;
  public first_name?: string;
  public last_name?: string;
  isUserSignedIn: boolean = false;
  showCommentBox: boolean = false;

  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private permission: PermissionService,
    private announcementService: AnnouncementsService,
    private authService: AuthenticationService,
    private router: Router
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      announcement: Announcement;
      comments: Comment[];
    };
    this.announcement = data.announcement;
    this.profile = data.profile;
    this.comments = this.announcement?.comments || [];
    this.slug = this.route.snapshot.params['slug'];

    this.comments.sort((a, b) => {
      if (!a.posted_date) return 1;
      if (!b.posted_date) return -1;

      const dateA = new Date(a.posted_date);
      const dateB = new Date(b.posted_date);

      return dateB.getTime() - dateA.getTime();
    });
  }

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isUserSignedIn = isAuthenticated;
    });
  }

  toggleCommentBox(open: boolean) {
    this.showCommentBox = open;
  }

  submitComment() {

    this.showCommentBox = false;

    if (this.userComment === '') {
      this.snackBar.open('Cannot submit an empty comment', '', {
        duration: 3000
      });
    }

    const publicUser = {
      id: this.profile.id!,
      first_name: this.profile.first_name!,
      last_name: this.profile.last_name!,
      pronouns: this.profile.pronouns!,
      email: this.profile.email!,
      github_avatar: this.profile.github_avatar
    };

    const newComment: Comment = {
      id: 0,
      text: this.userComment,
      posted_date: null,
      author_id: this.profile.id!,
      author: publicUser
    };
    this.announcementService
      .createComment(newComment, this.slug)
      .subscribe(() => {
        //  Stay on the announcement once the operation is complete.
        newComment.posted_date = new Date();
        this.comments.unshift(newComment);
        this.router.navigate(['/announcements/' + this.slug]);
        this.snackBar.open('Comment posted', '', { duration: 3000 });
      });
    this.userComment = '';
  }
}
