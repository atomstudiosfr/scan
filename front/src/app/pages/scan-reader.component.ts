import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScanService } from '../services/scan.service';

@Component({
  selector: 'app-scan-reader',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="selectedChapter" class="scan-reader">
      <ng-container *ngFor="let page of selectedChapter.pages">
        <img [src]="page" alt="Scan Page" class="scan-page">
      </ng-container>
    </div>
  `,
  styles: [`
    .scan-reader {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 100%;
    }
    .scan-page {
      max-width: 100%;
      height: auto;
      margin: 10px 0;
    }
  `]
})
export class ScanReaderComponent implements OnInit {
  selectedChapter: any;

  constructor(private scanService: ScanService) {}

  ngOnInit(): void {
    this.scanService.getSelectedScan().subscribe(scan => {
      if (scan && scan.pages) {
        this.selectedChapter = scan;
      }
    });
  }
}
