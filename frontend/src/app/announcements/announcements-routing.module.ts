import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnnouncementEditorComponent } from './announcement-editor/announcement-editor.component';
import { AnnouncementsDetailsPageComponent } from './announcements-details-page/announcements-details-page.component';
import { AnnouncementsPageComponent } from './announcements-page/announcements-page.component';

const routes: Routes = [
  AnnouncementsPageComponent.Route,
  AnnouncementsDetailsPageComponent.Route,
  AnnouncementEditorComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AnnouncementsRoutingModule {}
