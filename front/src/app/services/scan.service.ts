import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ScanService {
  private scans = new BehaviorSubject<any[]>([]);
  private selectedScan = new BehaviorSubject<any>(null);

  constructor() {
    this.fetchScans();
  }

  fetchScans() {
    // This is a mock implementation.
    // Replace with actual API call to your backend that reads the assets/scans directory.
    const scans = [
      {
        title: 'Manga 1',
        author: 'Author 1',
        description: 'Description 1',
        cover: 'assets/scans/manga1/cover.jpg',
        chapters: [
          {
            title: 'Chapter 1',
            pages: [
              'assets/scans/manga1/chapter1/1.webp',
              'assets/scans/manga1/chapter1/2.webp',
              'assets/scans/manga1/chapter1/3.webp',
              'assets/scans/manga1/chapter1/4.webp',
              'assets/scans/manga1/chapter1/5.webp'
            ]
          },
          {
            title: 'Chapter 2',
            pages: [
              'assets/scans/manga1/chapter2/1.webp',
              'assets/scans/manga1/chapter2/2.webp',
              'assets/scans/manga1/chapter2/3.webp',
              'assets/scans/manga1/chapter2/4.webp',
              'assets/scans/manga1/chapter2/5.webp'
            ]
          }
        ]
      },
      {
        title: 'Manga 2',
        author: 'Author 2',
        description: 'Description 2',
        cover: 'assets/scans/manga2/cover.jpg',
        chapters: [
          {
            title: 'Chapter 1',
            pages: [
              'assets/scans/manga2/chapter1/1.webp',
              'assets/scans/manga2/chapter1/2.webp',
              'assets/scans/manga2/chapter1/3.webp',
              'assets/scans/manga2/chapter1/4.webp',
              'assets/scans/manga2/chapter1/5.webp'
            ]
          }
        ]
      }
    ];
    this.scans.next(scans);
  }

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
