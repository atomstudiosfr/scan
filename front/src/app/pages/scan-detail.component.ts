import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ScanService } from '../services/scan.service';

@Component({
  selector: 'app-scan-detail',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="manga">
      <h1>{{manga.title}}</h1>
      <p><strong>Author:</strong> {{manga.author}}</p>
      <p><strong>Description:</strong> {{manga.description}}</p>
      <img [src]="manga.cover" alt="{{manga.title}} cover">
      <div *ngIf="chapters">
        <h2>Chapters</h2>
        <ul>
          <li *ngFor="let chapter of chapters">{{chapter.title}}</li>
        </ul>
      </div>
    </div>
  `,
  styles: [`
    img {
      max-width: 100%;
      height: auto;
    }
  `]
})
export class ScanDetailComponent implements OnInit {
  manga: any;
  chapters: any[];

  constructor(private route: ActivatedRoute, private scanService: ScanService) {}

  ngOnInit(): void {
    const mangaTitle = this.route.snapshot.paramMap.get('title');
    if (mangaTitle) {
      this.scanService.getScanDetails(mangaTitle).subscribe(data => {
        this.manga = {
          title: mangaTitle,
          author: data.author,
          description: data.description,
          cover: this.scanService.getMangaCover(mangaTitle)
        };
        this.chapters = data.chapters;
      });
    }
  }
}
