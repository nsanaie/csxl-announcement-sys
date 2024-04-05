import { Component, Input } from '@angular/core';
import { Announcement } from '../../announcement.model';
import { AnnouncementsService } from '../../announcements.service';
import { Router } from '@angular/router';

@Component({
  selector: 'announcement-card-widget',
  templateUrl: './announcement-card-widget.component.html',
  styleUrls: ['./announcement-card-widget.component.css']
})
export class AnnouncementCardWidgetComponent {
  @Input() announcement!: Announcement;
  constructor() {}
}
