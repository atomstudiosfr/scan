import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ScanService } from '../services/scan.service';

@Component({
  selector: 'app-chapter-viewer',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="chapter-viewer" *ngIf="pages">
      <h1>{{mangaTitle}} - {{chapterTitle}}</h1>
      <div class="pages">
        <img *ngFor="let page of pages" [src]="page" alt="Page">
      </div>
    </div>
  `,
  styles: [`
    .chapter-viewer {
      padding: 20px;
    }
    .pages {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .pages img {
      width: 100%;
      max-width: 800px;
      margin-bottom: 10px;
    }
  `]
})
export class ChapterViewerComponent implements OnInit {
  mangaTitle: string;
  chapterTitle: string;
  pages: string[];

  constructor(private route: ActivatedRoute, private scanService: ScanService) {}

  ngOnInit(): void {
    this.mangaTitle = this.route.snapshot.paramMap.get('manga');
    this.chapterTitle = this.route.snapshot.paramMap.get('chapter');
    this.scanService.getChapterDetails(this.mangaTitle).subscribe(data => {
      console.log(data)
      const chapter = data.find(ch => ch.chapter === this.chapterTitle);
      if (chapter) {
        this.pages = chapter.pages;
      }
    });
  }
}
