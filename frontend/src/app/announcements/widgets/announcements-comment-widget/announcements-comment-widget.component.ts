import { Component, Input, OnInit } from '@angular/core';
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
import { Announcement } from '../../announcement.model';
import { AnnouncementsService } from '../../announcements.service';
import { AnnouncementStatus } from '../../announcement.model';
import { announcementDetailResolver } from '../../announcement.resolver';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { PermissionService } from 'src/app/permission.service';
import { AnnouncementDetailsPageWidgetComponent } from '../announcement-details-page-widget/announcement-details-page-widget.component';
import { Profile } from 'src/app/models.module';
import { Comment } from '../../announcement.model';
import { AuthenticationService } from 'src/app/authentication.service';
import { MatCard } from '@angular/material/card';
import { MatCardTitle } from '@angular/material/card';
import { SocialMediaIcon } from 'src/app/shared/social-media-icon/social-media-icon.widget';

@Component({
  selector: 'app-announcements-comment-widget',
  standalone: true,
  imports: [],
  templateUrl: './announcements-comment-widget.component.html',
  styleUrl: './announcements-comment-widget.component.css'
})
export class AnnouncementsCommentWidgetComponent {
  @Input() comment?: Comment;
}
