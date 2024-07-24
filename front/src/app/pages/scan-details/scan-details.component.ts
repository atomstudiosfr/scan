import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ScanService} from '../../services/scan.service';

@Component({
  selector: 'app-scan-details',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="selectedScan">
      <h2>{{selectedScan.title}}</h2>
      <p>{{selectedScan.description}}</p>
    </div>
  `,
  styles: [`
    /* Add styles for scan details component */
  `]
})
export class ScanDetailsComponent implements OnInit {
  selectedScan: any;

  constructor(private scanService: ScanService) {}

  ngOnInit(): void {
    this.scanService.getSelectedScan().subscribe(scan => this.selectedScan = scan);
  }
}
