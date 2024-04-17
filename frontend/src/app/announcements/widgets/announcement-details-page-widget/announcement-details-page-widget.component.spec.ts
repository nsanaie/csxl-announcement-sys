import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnnouncementDetailsPageWidgetComponent } from './announcement-details-page-widget.component';

describe('AnnouncementDetailsPageWidgetComponent', () => {
  let component: AnnouncementDetailsPageWidgetComponent;
  let fixture: ComponentFixture<AnnouncementDetailsPageWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AnnouncementDetailsPageWidgetComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(AnnouncementDetailsPageWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
