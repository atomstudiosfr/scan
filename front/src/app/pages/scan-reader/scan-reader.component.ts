import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ScanService} from '../../services/scan.service';

@Component({
  selector: 'app-scan-reader',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './scan-reader.component.html',
  styleUrls: ['./scan-reader.component.css']
})
export class ScanReaderComponent implements OnInit {
  selectedScan: any;

  constructor(private scanService: ScanService) {}

  ngOnInit(): void {
    this.scanService.getSelectedScan().subscribe(scan => this.selectedScan = scan);
  }
}
