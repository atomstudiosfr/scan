import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ScanService {
  private baseUrl = 'https://raw.githubusercontent.com/atomstudiosfr/scan/main/assets/';
  private scanDataUrl = `${this.baseUrl}scans.json`;

  private scans = new BehaviorSubject<any[]>([]);
  private filteredScans = new BehaviorSubject<any[]>([]);
  private selectedScan = new BehaviorSubject<any | null>(null);

  constructor(private http: HttpClient) {
    this.loadScans();
  }

  private loadScans(): void {
    this.http.get<any[]>(this.scanDataUrl).subscribe(scans => {
      this.scans.next(scans);
      this.filteredScans.next(scans); // Initialize filteredScans with all scans
    });
  }

  getScans(): Observable<any[]> {
    return this.filteredScans.asObservable();
  }

  getScanDetails(mangaTitle: string): Observable<any> {
    const scanDetailsUrl = `${this.baseUrl}${mangaTitle}/scans.json`;
    return this.http.get<any>(scanDetailsUrl);
  }

  selectScan(scan: any): void {
    this.selectedScan.next(scan);
  }

  getSelectedScan(): Observable<any | null> {
    return this.selectedScan.asObservable();
  }

  getMangaCover(manga: string): string {
    return `${this.baseUrl}${manga}/cover.webp`;
  }

  getChapterPages(manga: string, chapter: string): Observable<string[]> {
    return this.getScanDetails(manga).pipe(
      map(details => {
        const chapterDetails = details.chapters.find((ch: any) => ch.title === `Chapter ${chapter}`);
        return chapterDetails ? chapterDetails.pages : [];
      })
    );
  }

  searchScans(query: string): void {
    const filtered = this.scans.getValue().filter(scan =>
      scan.title.toLowerCase().includes(query.toLowerCase())
    );
    this.filteredScans.next(filtered);
  }
}
