import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { Location } from '@angular/common';
import { Announcement } from '../../announcement.model';
import { AnnouncementsService } from '../../announcements.service';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route,
  Router
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Profile } from 'src/app/profile/profile.service';
import { PermissionService } from 'src/app/permission.service';
import { AuthenticationService } from 'src/app/authentication.service';

@Component({
  selector: 'app-announcement-details-page-widget',
  templateUrl: './announcement-details-page-widget.component.html',
  styleUrls: ['./announcement-details-page-widget.component.css']
})
export class AnnouncementDetailsPageWidgetComponent implements OnInit {
  isUserSignedIn: boolean = false;
  @Input() announcement?: Announcement;
  @Input() profile?: Profile;

  constructor(
    private permission: PermissionService,
    private location: Location,
    private snackBar: MatSnackBar,
    private announcementsService: AnnouncementsService,
    private authService: AuthenticationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isUserSignedIn = isAuthenticated;
    });
  }

  copyUrl() {
    if (this.announcement !== undefined) {
      this.announcementsService
        .updateShareCount(this.announcement.slug)
        .subscribe((data) => {
          console.log(data);
        });
      const urlString = 'http://localhost:1560' + this.location.path();
      navigator.clipboard
        .writeText(urlString)
        .then(() => {
          this.snackBar.open('URL copied to clipboard', '', { duration: 3000 });
        })
        .catch((error) => {
          console.error('Failed to copy URL to clipboard', error);
        });
    }
  }

  handleClick() {
    if (this.announcement && this.announcement.organization_slug) {
      console.log(this.announcement.organization_slug);
      // Assuming 'slug' is the property that identifies an organization
      const organizationSlug = this.announcement.organization_slug!;
      this.router.navigateByUrl(`/organizations/${organizationSlug}`);
    } else {
      // Handle the case when the clicked item is not recognized as an organization
      console.error('Clicked item is not recognized as an organization.');
      // Optionally, you can implement error handling or other logic here
    }
  }
}
