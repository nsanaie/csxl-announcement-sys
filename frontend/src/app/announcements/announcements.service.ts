import { Injectable } from '@angular/core';
import { Organization } from '../organization/organization.model';
import { Announcement } from './announcement.model';

@Injectable({
  providedIn: 'root'
})
export class AnnouncementsService {
  items: Announcement[] = [];

  addAnnouncement(announcement: Announcement) {
    this.items.push(announcement);
  }

  createAnnouncement(
    title: String,
    synopsis: String,
    body: String,
    organization: Organization
  ) {
    //create announcement method
  }

  updateAnnouncement(
    title: String,
    synopsis: String,
    body: String,
    organization: Organization
  ) {
    //update announcement method
  }

  getItems() {
    return this.items;
  }

  getItemById(id: number) {
    return this.items[id - 1];
  }

  constructor() {}
}
