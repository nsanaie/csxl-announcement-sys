import { Component, Input } from '@angular/core';
import { Comment } from '../../announcement.model';

@Component({
  selector: 'app-announcements-comment-widget',
  templateUrl: './announcements-comment-widget.component.html',
  styleUrl: './announcements-comment-widget.component.css'
})
export class AnnouncementsCommentWidgetComponent {
  @Input() comment?: Comment;
}
