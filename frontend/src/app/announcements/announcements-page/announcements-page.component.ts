import { Component } from '@angular/core';

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
}
