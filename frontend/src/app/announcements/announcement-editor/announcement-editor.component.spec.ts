import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnnouncementEditorComponent } from './announcement-editor.component';

describe('AnnouncementEditorComponent', () => {
  let component: AnnouncementEditorComponent;
  let fixture: ComponentFixture<AnnouncementEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AnnouncementEditorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AnnouncementEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
