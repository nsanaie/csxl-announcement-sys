import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnnouncementCardWidgetComponent } from './announcement-card-widget.component';

describe('AnnouncementCardWidgetComponent', () => {
  let component: AnnouncementCardWidgetComponent;
  let fixture: ComponentFixture<AnnouncementCardWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AnnouncementCardWidgetComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AnnouncementCardWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
