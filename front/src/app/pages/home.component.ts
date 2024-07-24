import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { ScanService } from '../services/scan.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, TableModule, ButtonModule],
  template: `
    <div class="home">
      <h1>Available Scans/Manga</h1>
      <p-table [value]="scans">
        <ng-template pTemplate="header">
          <tr>
            <th>Cover</th>
            <th>Title</th>
            <th>Author</th>
            <th>Actions</th>
          </tr>
        </ng-template>
        <ng-template pTemplate="body" let-scan>
          <tr>
            <td><img [src]="scan.cover" alt="{{scan.title}} cover" class="manga-cover"></td>
            <td>{{scan.title}}</td>
            <td>{{scan.author}}</td>
            <td>
              <button pButton type="button" label="View" (click)="viewScan(scan)"></button>
            </td>
          </tr>
        </ng-template>
      </p-table>
    </div>
  `,
  styles: [`
    .manga-cover {
      width: 100px;
      height: auto;
    }
  `]
})
export class HomeComponent implements OnInit {
  scans: any[];

  constructor(private scanService: ScanService, private router: Router) {}

  ngOnInit(): void {
    this.scanService.getScans().subscribe(data => this.scans = data);
  }

  viewScan(scan): void {
    this.scanService.selectScan(scan);
    this.router.navigate(['/viewer']);
  }
}
