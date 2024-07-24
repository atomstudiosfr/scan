import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ScanService {
  private scans = new BehaviorSubject<any[]>([]);
  private filteredScans = new BehaviorSubject<any[]>([]);
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
    this.filteredScans.next(scans);
  }

  getScans(): Observable<any[]> {
    return this.filteredScans.asObservable();
  }

  searchScans(query: string) {
    const filtered = this.scans.getValue().filter(scan => scan.title.toLowerCase().includes(query.toLowerCase()));
    this.filteredScans.next(filtered);
  }

  selectScan(scan): void {
    this.selectedScan.next(scan);
  }

  getSelectedScan(): Observable<any> {
    return this.selectedScan.asObservable();
  }
}
