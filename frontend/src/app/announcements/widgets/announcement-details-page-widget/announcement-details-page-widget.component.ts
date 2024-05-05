import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { Location } from '@angular/common';
import { Announcement, UpvoteBoolean } from '../../announcement.model';
import { AnnouncementsService } from '../../announcements.service';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  Navigation,
  ResolveFn,
  Route,
  Router
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
import { PermissionService } from 'src/app/permission.service';
import { AuthenticationService } from 'src/app/authentication.service';
import { AnnouncementStatus } from '../../announcement.model';

@Component({
  selector: 'app-announcement-details-page-widget',
  templateUrl: './announcement-details-page-widget.component.html',
  styleUrls: ['./announcement-details-page-widget.component.css']
})
export class AnnouncementDetailsPageWidgetComponent implements OnInit {
  isUserSignedIn: boolean = false;
  didUserUpvote: boolean = false;
  didUserFavorite: boolean = false;

  @Input() announcement?: Announcement;
  @Input() profile?: Profile;
  @Input() commentBox?: boolean;
  @Output() openCommentBox = new EventEmitter<boolean>();

  public AnnouncementStatus = AnnouncementStatus;

  constructor(
    private permission: PermissionService,
    private location: Location,
    private snackBar: MatSnackBar,
    private announcementsService: AnnouncementsService,
    private profileService: ProfileService,
    private authService: AuthenticationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isUserSignedIn = isAuthenticated;
    });
    if (this.isUserSignedIn && this.announcement !== undefined) {
      this.announcementsService
        .checkUserUpvote(this.announcement.slug)
        .subscribe((data) => {
          this.didUserUpvote = data.upvoted;
        });
      this.announcementsService
        .checkUserFavorite(this.announcement.slug)
        .subscribe((data) => {
          this.didUserFavorite = data.upvoted;
        });
    }
  }

  goBack(): void {
    this.location.back();
  }

  handleCommentClick() {
    this.openCommentBox.emit(!this.commentBox);
  }

  handleAddFavoriteClick() {
    if (
      this.isUserSignedIn &&
      this.announcement !== undefined &&
      !this.didUserFavorite
    ) {
      this.announcementsService
        .addUserFavorite(this.announcement.slug)
        .subscribe((data) => {
          this.didUserFavorite = data.upvoted;
        });
    }
  }

  handleRemoveFavoriteClick() {
    if (
      this.isUserSignedIn &&
      this.announcement !== undefined &&
      this.didUserFavorite
    ) {
      this.announcementsService
        .removeUserFavorite(this.announcement.slug)
        .subscribe((data) => {
          this.didUserFavorite = data.upvoted;
        });
    }
  }

  handleAddUpvoteClick() {
    if (
      this.isUserSignedIn &&
      this.announcement !== undefined &&
      !this.didUserUpvote
    ) {
      const prevUpvote = this.didUserUpvote;
      this.announcementsService
        .incrementUpvoteCount(this.announcement.slug)
        .subscribe((data) => {
          this.didUserUpvote = data.upvoted;
          if (
            prevUpvote != this.didUserUpvote &&
            this.announcement !== undefined &&
            this.announcement.upvote_count !== null
          ) {
            this.announcement.upvote_count += 1;
          }
        });
    }
  }

  handleRemoveUpvoteClick() {
    if (
      this.isUserSignedIn &&
      this.announcement !== undefined &&
      this.didUserUpvote
    ) {
      const prevUpvote = this.didUserUpvote;
      this.announcementsService
        .decrementUpvoteCount(this.announcement.slug)
        .subscribe((data) => {
          this.didUserUpvote = data.upvoted;
          if (
            prevUpvote != this.didUserUpvote &&
            this.announcement !== undefined &&
            this.announcement.upvote_count !== null
          ) {
            this.announcement.upvote_count -= 1;
          }
        });
    }
  }

  handleShareClick() {
    if (this.announcement !== undefined) {
      this.announcementsService
        .updateShareCount(this.announcement.slug)
        .subscribe();
      const urlString = window.location.href;
      navigator.clipboard
        .writeText(urlString)
        .then(() => {
          this.snackBar.open('URL copied to clipboard', '', { duration: 3000 });
        })
        .catch((error) => {
          console.error('Failed to copy URL to clipboard', error);
          this.snackBar.open('Failed to copy URL to clipboard', '', {
            duration: 3000
          });
        });
    }
  }

  handleOrgClick() {
    if (this.announcement && this.announcement.organization_slug) {
      const organizationSlug = this.announcement.organization_slug!;
      this.router.navigateByUrl(`/organizations/${organizationSlug}`);
    } else {
      console.error('Clicked item is not recognized as an organization.');
    }
  }
}
