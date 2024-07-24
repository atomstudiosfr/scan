import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenubarModule } from 'primeng/menubar';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { MenuItem } from 'primeng/api';
import { FormsModule } from '@angular/forms';
import { ScanService } from '../services/scan.service';
import { ThemeService } from '../services/theme.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, MenubarModule, InputTextModule, ButtonModule, FormsModule],
  template: `
    <p-menubar [model]="items">
      <ng-template pTemplate="start">
        <img src="assets/logo.webp" height="40" alt="logo">
      </ng-template>
      <ng-template pTemplate="end">
        <input type="text" pInputText placeholder="Search manga..." [(ngModel)]="searchQuery" (ngModelChange)="onSearch()">
        <button pButton icon="pi pi-moon" class="p-button-rounded p-button-outlined" (click)="toggleDarkMode()"></button>
      </ng-template>
    </p-menubar>
  `,
  styles: [`
    :host {
      display: block;
    }
    p-menubar {
      background: var(--surface-a);
      color: var(--text-color);
    }
  `]
})
export class HeaderComponent implements OnInit {
  items: MenuItem[];
  searchQuery: string = '';
  currentTheme: string = 'light';

  constructor(private scanService: ScanService, private themeService: ThemeService) {}

  ngOnInit() {
    this.items = [
      {label: 'Home', icon: 'pi pi-fw pi-home', routerLink: ['/']},
      {label: 'Viewer', icon: 'pi pi-fw pi-eye', routerLink: ['/viewer']}
    ];
    this.applyTheme();
  }

  onSearch() {
    this.scanService.searchScans(this.searchQuery);
  }

  toggleDarkMode() {
    this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.themeService.switchTheme(this.currentTheme);
    localStorage.setItem('theme', this.currentTheme);
  }

  applyTheme() {
    const theme = localStorage.getItem('theme') || 'light';
    this.currentTheme = theme;
    this.themeService.switchTheme(theme);
  }
}
