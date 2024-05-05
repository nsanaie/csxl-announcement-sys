import { Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AdminAnnouncementService } from '../admin-announcements-service';
import {
  Announcement,
  AnnouncementStatus
} from 'src/app/announcements/announcement.model';
import { Observable } from 'rxjs';
import { AnnouncementsService } from 'src/app/announcements/announcements.service';
import { Input } from '@angular/core';
import { map } from 'rxjs';
import { Profile } from 'src/app/profile/profile.service';
import { profileResolver } from 'src/app/profile/profile.resolver';

@Component({
  selector: 'app-admin-announcements-list',
  templateUrl: './admin-announcements-list.component.html',
  styleUrls: ['./admin-announcements-list.component.css']
})
export class AdminAnnouncementsListComponent {
  @Input() announcement?: Announcement;

  public announcements$: Observable<Announcement[]>;

  public displayedColumns: string[] = ['name'];

  public AnnouncementStatus = AnnouncementStatus;

  public profile: Profile;

  public static Route = {
    path: 'announcements',
    component: AdminAnnouncementsListComponent,
    resolve: {
      profile: profileResolver
    },
    title: 'Announcement Administration',
    canActivate: [permissionGuard('announcements.list', 'announcements')]
  };

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private adminAnnouncementService: AdminAnnouncementService,
    private announcementsService: AnnouncementsService,
    private route: ActivatedRoute
  ) {
    this.announcements$ = adminAnnouncementService.announcements$.pipe(
      map((announcements) =>
        announcements.filter(
          (announcement) =>
            announcement.status === AnnouncementStatus.PUBLISHED ||
            announcement.status === AnnouncementStatus.ARCHIVED ||
            announcement.status === AnnouncementStatus.DRAFT
        )
      )
    );
    adminAnnouncementService.list();
    const data = this.route.snapshot.data as {
      profile: Profile;
    };
    this.profile = data.profile;
  }

  createAnnouncement(): void {
    this.router.navigate(['announcements', 'new', 'edit']);
  }

  /** Delete an announcement object from the backend database table using the backend HTTP post request.
   * @param announcement_id: unique number representing the updated announcement
   * @returns void
   */
  deleteAnnouncement(announcement: Announcement): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this announcement?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.adminAnnouncementService
        .deleteAnnouncement(announcement)
        .subscribe(() => {
          this.snackBar.open('This announcement has been deleted.', '', {
            duration: 2000
          });
        });
    });
  }

  archiveAnnouncement(announcement: Announcement): void {
    if (announcement.status == AnnouncementStatus.PUBLISHED) {
      let confirmUpdate = this.snackBar.open(
        'Are you sure you want to archive this announcement?',
        'Archive',
        { duration: 15000 }
      );
      confirmUpdate.onAction().subscribe(() => {
        announcement.status = AnnouncementStatus.ARCHIVED;
        this.adminAnnouncementService.updateAnnouncement(announcement);
        this.snackBar.open('Announcement Archived', '', {
          duration: 15000
        });
      });
    } else {
      let confirmUpdate = this.snackBar.open(
        'Are you sure you want to unarchive this announcement?',
        'Unarchive',
        { duration: 15000 }
      );
      confirmUpdate.onAction().subscribe(() => {
        announcement.status = AnnouncementStatus.PUBLISHED;
        this.adminAnnouncementService.updateAnnouncement(announcement);
        this.snackBar.open('Announcement Unarchived', '', {
          duration: 15000
        });
      });
    }
  }

  // goToDetails(announcement: Announcement): void {
  //   if (announcement.status == AnnouncementStatus.PUBLISHED) {
  //     this.router.navigateByUrl(`/announcements/${announcement.slug}`);
  //   } else if (announcement.status == AnnouncementStatus.ARCHIVED) {
  //     this.adminAnnouncementService.getAdminAnnouncement(announcement);
  //   }
  // }
}
