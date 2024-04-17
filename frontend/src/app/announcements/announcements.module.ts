import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AnnouncementsPageComponent } from './announcements-page/announcements-page.component';
import { AnnouncementsRoutingModule } from './announcements-routing.module';
import { AnnouncementCardWidgetComponent } from './widgets/announcement-card-widget/announcement-card-widget.component';
import { AnnouncementsDetailsPageComponent } from './announcements-details-page/announcements-details-page.component';
import { AnnouncementDetailsPageWidgetComponent } from './widgets/announcement-details-page-widget/announcement-details-page-widget.component';

@NgModule({
  declarations: [
    AnnouncementsPageComponent,
    AnnouncementCardWidgetComponent,
    AnnouncementsDetailsPageComponent,
    AnnouncementDetailsPageWidgetComponent
  ],
  imports: [
    CommonModule,
    AnnouncementsRoutingModule,
    MatCardModule,
    MatTableModule,
    MatTabsModule,
    MatDialogModule,
    MatButtonModule,
    MatListModule,
    MatAutocompleteModule,
    MatSelectModule,
    MatFormFieldModule,
    MatPaginatorModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatTooltipModule
  ]
})
export class AnnouncementsModule {}
