import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenubarModule } from 'primeng/menubar';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, MenubarModule],
  template: `
    <p-menubar [model]="items">
      <ng-template pTemplate="start">
        <img src="assets/logo.png" height="40" alt="logo">
      </ng-template>
    </p-menubar>
  `,
  styles: [`
    :host {
      display: block;
    }
    p-menubar {
      background: #007ad9;
      color: #fff;
    }
  `]
})
export class HeaderComponent {
  items: MenuItem[];

  ngOnInit() {
    this.items = [
      {label: 'Home', icon: 'pi pi-fw pi-home', routerLink: ['/']},
      {label: 'Viewer', icon: 'pi pi-fw pi-eye', routerLink: ['/viewer']}
    ];
  }
}
