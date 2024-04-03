import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnnouncementsPageComponent } from './announcements-page.component';

describe('AnnouncementsPageComponent', () => {
  let component: AnnouncementsPageComponent;
  let fixture: ComponentFixture<AnnouncementsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AnnouncementsPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AnnouncementsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
