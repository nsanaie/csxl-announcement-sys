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
import { Observable } from 'rxjs';
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
    // children: [
    //   {
    //     path: '',
    //     title: titleResolver,
    //     component: AnnouncementsDetailsPageComponent
    //   }
    // ]
  };
  displayedComment: string = '';

  public announcement: Announcement;
  public profile: Profile;
  public first_name?: string;
  public last_name?: string;
  isUserSignedIn: boolean = false;

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
  }

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isUserSignedIn = isAuthenticated;
    });
  }

  submitComment() {
    // Logic to submit the comment
    // For demonstration purposes, let's create a new comment object and add it to the comments array
    let posted_date: Date = new Date();
    let date_long_string = posted_date.toLocaleDateString();
    let date_string = `${posted_date.getFullYear()}-${this.addLeadingZero(
      posted_date.getMonth() + 1
    )}-${this.addLeadingZero(posted_date.getDate())}`;

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
      posted_date: date_string, // You can replace this with the actual date
      author_id: this.profile.id!,
      author: publicUser
    };
    // Clear the input field after submitting the comment
    this.announcementService
      .createComment(newComment, this.slug)
      .subscribe(() => {
        //  Stay on the announcement once the operation is complete.
        this.comments.push(newComment);
        this.router.navigate(['/announcements/' + this.slug]);
      });
    this.userComment = '';
  }
}
