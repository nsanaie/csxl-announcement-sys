import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Announcement } from '../announcement.model';
import { AnnouncementsService } from '../announcements.service';

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

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private announcmentsService: AnnouncementsService
  ) {}

  createAnnouncement(): void {
    // Navigate to the announcement editor for a new announcement (slug = create)
    this.router.navigate(['announcements', '1', 'edit']);
  }
}
