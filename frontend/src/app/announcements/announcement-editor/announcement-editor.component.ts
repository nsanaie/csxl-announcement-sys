import { Component } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  CanActivateFn,
  Route,
  Router,
  RouterStateSnapshot
} from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { PermissionService } from 'src/app/permission.service';
import { Announcement } from '../announcement.model';
import { AnnouncementsService } from '../announcements.service';
@Component({
  selector: 'app-announcement-editor',
  templateUrl: './announcement-editor.component.html',
  styleUrls: ['./announcement-editor.component.css']
})
export class AnnouncementEditorComponent {
  public static Route: Route = {
    path: '1/edit',
    component: AnnouncementEditorComponent
  };

  public announcement: Announcement;

  announcement_slug: string = '1';

  // public announcementForm = this.formBuilder.group(
  //    title: this.title,

  //  );

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private announcementService: AnnouncementsService
  ) {
    const data = this.route.snapshot.data as {
      announcement: Announcement;
    };
    this.announcement = data.announcement;

    let announcement_slug = this.route.snapshot.params['slug'];
    this.announcement_slug = announcement_slug;
  }
}
