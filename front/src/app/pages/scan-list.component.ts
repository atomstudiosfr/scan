import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import {ScanService} from '../services/scan.service';

@Component({
  selector: 'app-scan-list',
  standalone: true,
  imports: [CommonModule, TableModule, ButtonModule],
  template: `
    <p-table [value]="scans">
      <ng-template pTemplate="header">
        <tr>
          <th>Title</th>
          <th>Author</th>
          <th>Actions</th>
        </tr>
      </ng-template>
      <ng-template pTemplate="body" let-scan>
        <tr>
          <td>{{scan.title}}</td>
          <td>{{scan.author}}</td>
          <td>
            <button pButton type="button" label="View" (click)="viewScan(scan)"></button>
          </td>
        </tr>
      </ng-template>
    </p-table>
  `,
  styles: [`
    /* Add styles for scan list component */
  `]
})
export class ScanListComponent implements OnInit {
  scans: any[];

  constructor(private scanService: ScanService) {}

  ngOnInit(): void {
    this.scanService.getScans().subscribe(data => this.scans = data);
  }

  viewScan(scan): void {
    this.scanService.selectScan(scan);
  }
}
