import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnnouncementsDetailsPageComponent } from './announcements-details-page.component';

describe('AnnouncementsDetailsPageComponent', () => {
  let component: AnnouncementsDetailsPageComponent;
  let fixture: ComponentFixture<AnnouncementsDetailsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AnnouncementsDetailsPageComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(AnnouncementsDetailsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
