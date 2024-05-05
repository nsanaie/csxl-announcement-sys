import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnnouncementsCommentWidgetComponent } from './announcements-comment-widget.component';

describe('AnnouncementsCommentWidgetComponent', () => {
  let component: AnnouncementsCommentWidgetComponent;
  let fixture: ComponentFixture<AnnouncementsCommentWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AnnouncementsCommentWidgetComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AnnouncementsCommentWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
