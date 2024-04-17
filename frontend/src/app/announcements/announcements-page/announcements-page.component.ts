import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Announcement } from '../announcement.model';
import { AnnouncementsService } from '../announcements.service';
import { AnnouncementStatus } from '../announcement.model';
import { profileResolver } from 'src/app/profile/profile.resolver';
import {
  announcementDetailResolver,
  announcementResolver
} from '../announcement.resolver';
import { Profile } from 'src/app/models.module';
import { NumberSymbol } from '@angular/common';
import { AuthenticationService } from 'src/app/authentication.service';

@Component({
  selector: 'app-announcements-page',
  templateUrl: './announcements-page.component.html',
  styleUrls: ['./announcements-page.component.css']
})
export class AnnouncementsPageComponent {
  public static Route = {
    path: '',
    title: 'Announcements',
    component: AnnouncementsPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver, announcements: announcementResolver }
  };

  public announcements: Announcement[];

  public profile: Profile;

  public permValues: Map<number, number> = new Map();

  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar
  ) {
    const data = this.route.snapshot.data as {
      profile: Profile;
      announcements: Announcement[];
    };
    this.profile = data.profile;
    this.announcements = data.announcements;
  }
}
