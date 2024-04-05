import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Announcement } from '../announcement.model';
import { AnnouncementsService } from '../announcements.service';
import { AnnouncementStatus } from '../announcement.model';

@Component({
  selector: 'app-announcements-page',
  templateUrl: './announcements-page.component.html',
  styleUrls: ['./announcements-page.component.css']
})
export class AnnouncementsPageComponent {
  public static Route = {
    path: '',
    title: 'Announcement Tools',
    component: AnnouncementsPageComponent,
    canActivate: []
  };

  public announcements: Announcement[];

  constructor() {
    this.announcements = [
      {
        id: 1,
        title: 'Apply for App Team Carolina!',
        synopsis:
          'Applications are OUT for the Spring semester! Apply by March 1st!',
        body: 'Sample body',
        organization: null,
        image: null,
        state: AnnouncementStatus.PUBLISHED,
        viewCount: null,
        commentCount: null,
        shareCount: null,
        publishedDate: null,
        editedDate: null
      },
      {
        id: 2,
        title: 'Apply for PM Club!',
        synopsis:
          'Applications are OUT for the Spring semester! Apply by March 1st!',
        body: 'Sample body',
        organization: null,
        image: null,
        state: AnnouncementStatus.PUBLISHED,
        viewCount: null,
        commentCount: null,
        shareCount: null,
        publishedDate: null,
        editedDate: null
      }
    ];
  }

  // createAnnouncement(): void {
  //   // Navigate to the announcement editor for a new announcement (slug = create)
  //   this.router.navigate(['announcements', '1', 'edit']);
  // }
}
