import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import {
  Announcement,
  AnnouncementStatus,
  AnnouncementSortMethod
} from '../announcement.model';
import { AnnouncementsService } from '../announcements.service';
import { AuthenticationService } from 'src/app/authentication.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import {
  announcementDetailResolver,
  announcementResolver
} from '../announcement.resolver';
import { Profile } from 'src/app/models.module';
import { NumberSymbol } from '@angular/common';
import { ProfileService } from 'src/app/profile/profile.service';

@Component({
  selector: 'app-announcements-page',
  templateUrl: './announcements-page.component.html',
  styleUrls: ['./announcements-page.component.css']
})
export class AnnouncementsPageComponent implements OnInit {
  public static Route = {
    path: '',
    title: 'Announcements',
    component: AnnouncementsPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver, announcements: announcementResolver }
  };

  public announcements: Announcement[];
  public filteredAnnouncements: Announcement[];
  public favoriteAnnouncements: number[];
  public profile: Profile;

  public searchBarQuery = '';
  public sortMethod: AnnouncementSortMethod;
  public favoriteToggle: boolean;
  public currentPage: number;
  public itemsPerPage: number = 6;
  public totalPages: number;

  public permValues: Map<number, number> = new Map();

  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private announcementService: AnnouncementsService,
    private authService: AuthenticationService,
    private profileService: ProfileService
  ) {
    const data = this.route.snapshot.data as {
      profile: Profile;
      announcements: Announcement[];
    };
    this.profile = data.profile;
    this.announcements = data.announcements;
    this.favoriteAnnouncements = [];
    this.filteredAnnouncements = this.announcements;
    this.totalPages = Math.ceil(this.announcements.length / this.itemsPerPage);
    this.sortMethod = announcementService.getSortMethod();
    this.currentPage = announcementService.getCurrentPage();
    this.favoriteToggle = announcementService.getFavoriteToggle();
  }

  ngOnInit() {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.profileService.refreshProfile(isAuthenticated);
    });

    this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        this.favoriteAnnouncements = profile.favorite_announcements_id;
      }
    });
    this.updatePage();
  }

  onPageChange(pageNumber: number) {
    if (pageNumber >= 1 && pageNumber <= this.totalPages) {
      this.currentPage = this.announcementService.setCurrentPage(pageNumber);
    }
    this.updatePage();
  }

  updatePage(): void {
    this.filteredAnnouncements = this.announcements.filter((announcement) =>
      this.isAnnouncementMatchSearchQuery(announcement, this.searchBarQuery)
    );

    this.sortAnnouncements();

    this.filterFavorites();

    this.totalPages = Math.ceil(
      this.filteredAnnouncements.length / this.itemsPerPage
    );

    if (this.currentPage > this.totalPages) {
      this.currentPage = this.announcementService.setCurrentPage(
        this.totalPages
      );
    }

    if (this.currentPage === 0 && this.totalPages > 0) {
      this.currentPage = 1;
    }

    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.filteredAnnouncements = this.filteredAnnouncements.slice(
      startIndex,
      endIndex
    );
  }

  isAnnouncementMatchSearchQuery(
    announcement: Announcement,
    searchQuery: string
  ): boolean {
    const fullName =
      (
        announcement.author?.first_name +
        ' ' +
        announcement.author?.last_name
      ).toLowerCase() || '';
    const lowercaseSearchQuery = searchQuery.toLowerCase();

    return (
      announcement.headline.toLowerCase().includes(lowercaseSearchQuery) ||
      announcement.syn.toLowerCase().includes(lowercaseSearchQuery) ||
      announcement.organization?.name
        .toLowerCase()
        .includes(lowercaseSearchQuery) ||
      fullName.includes(lowercaseSearchQuery)
    );
  }

  isFirstPage(): boolean {
    return this.currentPage === 1;
  }

  isLastPage(): boolean {
    return this.currentPage === this.totalPages;
  }

  sortAnnouncements() {
    if (this.sortMethod === AnnouncementSortMethod.UPVOTES) {
      this.filteredAnnouncements = this.filteredAnnouncements.sort(
        (a, b) => (b.upvote_count || 0) - (a.upvote_count || 0)
      );
    } else if (this.sortMethod === AnnouncementSortMethod.VIEWS) {
      this.filteredAnnouncements = this.filteredAnnouncements.sort(
        (a, b) => (b.view_count || 0) - (a.view_count || 0)
      );
    } else if (this.sortMethod === AnnouncementSortMethod.NEWEST) {
      this.filteredAnnouncements = this.filteredAnnouncements.sort((a, b) => {
        if (!a.published_date) return 1;
        if (!b.published_date) return -1;

        const dateA = new Date(a.published_date);
        const dateB = new Date(b.published_date);

        return dateB.getTime() - dateA.getTime();
      });
    }
  }

  filterFavorites() {
    if (this.favoriteToggle) {
      const filteredList = this.filteredAnnouncements.filter((announcement) => {
        if (announcement.id !== undefined && announcement.id !== null) {
          return this.favoriteAnnouncements.includes(announcement.id);
        }
        return false;
      });
      this.filteredAnnouncements = filteredList;
    }
  }

  handleSortClick() {
    if (this.sortMethod === AnnouncementSortMethod.NEWEST) {
      this.sortMethod = this.announcementService.setSortMethod(
        AnnouncementSortMethod.UPVOTES
      );
    } else if (this.sortMethod === AnnouncementSortMethod.UPVOTES) {
      this.sortMethod = this.announcementService.setSortMethod(
        AnnouncementSortMethod.VIEWS
      );
    } else if (this.sortMethod === AnnouncementSortMethod.VIEWS) {
      this.sortMethod = this.announcementService.setSortMethod(
        AnnouncementSortMethod.NEWEST
      );
    }
    this.updatePage();
  }

  handleFavoriteClick() {
    this.favoriteToggle = this.announcementService.setFavoriteToggle(
      !this.favoriteToggle
    );
    this.updatePage();
  }
}
