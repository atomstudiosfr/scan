import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ScanService {
  private scans = new BehaviorSubject<any[]>([
    { title: 'Scan 1', author: 'Author 1', description: 'Description 1', pages: [{ imageUrl: 'assets/scan1-page1.jpg' }, { imageUrl: 'assets/scan1-page2.jpg' }] },
    { title: 'Scan 2', author: 'Author 2', description: 'Description 2', pages: [{ imageUrl: 'assets/scan2-page1.jpg' }, { imageUrl: 'assets/scan2-page2.jpg' }] }
  ]);
  private selectedScan = new BehaviorSubject<any>(null);

  getScans(): Observable<any[]> {
    return this.scans.asObservable();
  }

  selectScan(scan): void {
    this.selectedScan.next(scan);
  }

  getSelectedScan(): Observable<any> {
    return this.selectedScan.asObservable();
  }
}
