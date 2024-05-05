import { Component, Input, OnInit } from '@angular/core';
import { Announcement } from '../../announcement.model';
import { AnnouncementsService } from '../../announcements.service';
import { AuthenticationService } from 'src/app/authentication.service';
import { Router } from '@angular/router';
import { Profile } from 'src/app/models.module';
import { AnnouncementStatus } from '../../announcement.model';

@Component({
  selector: 'announcement-card-widget',
  templateUrl: './announcement-card-widget.component.html',
  styleUrls: ['./announcement-card-widget.component.css']
})
export class AnnouncementCardWidgetComponent implements OnInit {
  @Input() announcement?: Announcement;
  @Input() profile?: Profile;
  @Input() profilePermission!: Map<number, number>;
  isUserSignedIn: boolean = false;

  public AnnouncementStatus = AnnouncementStatus;

  constructor(
    private router: Router,
    private authService: AuthenticationService,
    private announcementsService: AnnouncementsService
  ) {}

  handleOrganizationClick() {
    if (this.announcement && this.announcement.organization_slug) {
      const organizationSlug = this.announcement.organization_slug!;
      this.router.navigateByUrl(`/organizations/${organizationSlug}`);
    } else {
      console.error('Clicked item is not recognized as an organization.');
    }
  }

  handleDetailsClick() {
    if (this.announcement && this.announcement.slug) {
      if (this.isUserSignedIn) {
        this.announcementsService
          .updateViewCount(this.announcement.slug)
          .subscribe();
      }
      this.router.navigateByUrl(`/announcements/${this.announcement.slug!}`);
    } else {
      console.error('Clicked item is not recognized as an announcement.');
    }
  }

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isUserSignedIn = isAuthenticated;
    });
  }
}
