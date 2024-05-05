import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminAnnouncementsListComponent } from './admin-announcements-list.component';

describe('AdminAnnouncementsListComponent', () => {
  let component: AdminAnnouncementsListComponent;
  let fixture: ComponentFixture<AdminAnnouncementsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AdminAnnouncementsListComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(AdminAnnouncementsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
