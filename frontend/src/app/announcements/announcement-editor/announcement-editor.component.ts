import { Component, inject } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  CanActivateFn,
  Route,
  Router,
  RouterStateSnapshot
} from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { PermissionService } from 'src/app/permission.service';
import { Announcement } from '../announcement.model';
import { AnnouncementsService } from '../announcements.service';
import { Profile, PublicProfile } from 'src/app/profile/profile.service';
import { announcementDetailResolver } from '../announcement.resolver';
import { TransitionCheckState } from '@angular/material/checkbox';
import { Organization } from 'src/app/organization/organization.model';
import { OrganizationService } from 'src/app/organization/organization.service';
import { OrganizationModule } from 'src/app/organization/organization.module';
import { AnnouncementStatus } from '../announcement.model';

const canActivateEditor: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  /** Determine if page is viewable by user based on permissions */

  let slug: string = route.params['slug'];

  if (slug === 'new') {
    return inject(PermissionService).check(
      'announcement.create',
      'announcement'
    );
  } else {
    return inject(PermissionService).check(
      'announcement.update',
      `announcement/${slug}`
    );
  }
};

@Component({
  selector: 'app-announcement-editor',
  templateUrl: './announcement-editor.component.html',
  styleUrls: ['./announcement-editor.component.css']
})
export class AnnouncementEditorComponent {
  organizations?: Organization[];
  selectedFileName: string | undefined;

  public static Route: Route = {
    path: ':slug/edit',
    component: AnnouncementEditorComponent,
    title: 'Announcement Editor',
    canActivate: [canActivateEditor],
    resolve: {
      profile: profileResolver,
      announcement: announcementDetailResolver
    }
  };

  public AnnouncementStatus = AnnouncementStatus;

  public announcement: Announcement;

  public profile: Profile | null = null;

  public org: Organization | null = null;

  announcement_slug: string = 'new';

  headline = new FormControl('', [Validators.required]);
  slug = new FormControl('', [
    Validators.required,
    Validators.pattern('^(?!new$)[a-z0-9-]+$')
  ]);
  syn = new FormControl('', [Validators.required]);
  body = new FormControl('', [Validators.required]);
  organization = new FormControl(<Organization | null>null);
  image = new FormControl(<string | null>'');

  author_id = new FormControl(0);
  organization_id: number | null = 0;
  state: AnnouncementStatus = AnnouncementStatus.DRAFT;

  public announcementForm = this.formBuilder.group({
    headline: this.headline,
    slug: this.slug,
    body: this.body,
    syn: this.syn,
    organization: this.organization,
    author_id: this.profile?.id,
    organization_id: 1,
    state: this.state,
    image: this.image
  });

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private announcementService: AnnouncementsService,
    private organizationService: OrganizationService
  ) {
    const data = this.route.snapshot.data as {
      profile: Profile;
      announcement: Announcement;
    };
    this.profile = data.profile;
    this.announcement = data.announcement;

    this.getOrganizations();

    let announcement_slug = this.route.snapshot.params['slug'];
    this.announcement_slug = announcement_slug;

    if (announcement_slug == 'new') {
      this.announcementForm.setValue({
        headline: '',
        slug: '',
        body: '',
        syn: '',
        organization: null,
        author_id: this.profile.id,
        organization_id: null,
        state: AnnouncementStatus.DRAFT,
        image: ''
      });
    } else {
      this.announcementForm.setValue({
        headline: this.announcement.headline,
        slug: this.announcement.slug,
        body: this.announcement.body,
        syn: this.announcement.syn,
        organization: this.announcement.organization,
        author_id: this.announcement.author_id,
        organization_id: this.announcement.organization_id,
        state: this.announcement.status,
        image: this.announcement.organization?.logo ?? this.announcement.image
      });
    }
  }

  changeId(id: number | null, image: string | null) {
    this.organization_id = id;
    this.announcement.image = image;
  }

  private getOrganizations() {
    this.organizationService.getOrganizations().subscribe((data) => {
      this.organizations = data;
    });
  }

  onSubmit(): void {
    if (this.announcementForm.valid) {
      if (this.announcement.status != AnnouncementStatus.ARCHIVED) {
        this.announcement.status = AnnouncementStatus.PUBLISHED;
      }
      Object.assign(this.announcement, this.announcementForm.value);
      if (this.organization_id) {
        this.announcement.organization_id = this.organization_id;
        if (this.announcement.image == null || this.announcement.image == '') {
          this.announcement.image = this.announcement.organization?.logo ?? '';
        }
      }
      this.announcement.organization = null;
      if (this.announcement_slug == 'new') {
        this.announcementService
          .createAnnouncement(this.announcement)
          .subscribe({
            next: (announcement) => this.onSuccess(announcement),
            error: (err) => this.onError(err)
          });
      } else {
        this.announcementService
          .updateAnnouncement(this.announcement)
          .subscribe({
            next: (announcement) => this.onSuccess(announcement),
            error: (err) => this.onError(err)
          });
      }
    }
  }

  onSaveAsDraft(): void {
    if (this.announcementForm.valid) {
      this.announcement.status = AnnouncementStatus.DRAFT;
      Object.assign(this.announcement, this.announcementForm.value);
      if (this.announcement_slug == 'new') {
        this.announcementService
          .createAnnouncement(this.announcement)
          .subscribe({
            next: (announcement) => this.onSuccess(announcement),
            error: (err) => this.onError(err)
          });
      } else {
        this.announcementService
          .updateAnnouncement(this.announcement)
          .subscribe({
            next: (announcement) => this.onSuccess(announcement),
            error: (err) => this.onError(err)
          });
      }
    }
  }

  onCancel(): void {
    this.router.navigate([`admin/announcements/`]);
  }

  generateSlug(): void {
    const title = this.announcementForm.controls['headline'].value;
    const slug = this.announcementForm.controls['slug'].value;
    if (title && !slug) {
      var generatedSlug = title.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-');
      this.announcementForm.setControl('slug', new FormControl(generatedSlug));
    }
  }

  private onSuccess(announcement: Announcement): void {
    this.router.navigate(['/announcements/', announcement.slug]);

    let message: string =
      this.announcement_slug === 'new'
        ? 'Announcement Created'
        : 'Announcement Updated';

    this.snackBar.open(message, '', { duration: 2000 });
  }

  private onError(err: any): void {
    let message: string =
      this.announcement_slug === 'new'
        ? 'Error: Annoucnement Not Created'
        : 'Error: Announcement Not Updated';

    this.snackBar.open(message, '', {
      duration: 2000
    });
  }
}
