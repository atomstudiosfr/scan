import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home.component';
import { ScanDetailComponent } from './pages/scan-detail.component';
import { ChapterViewerComponent } from './pages/chapter-viewer.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'viewer/:title', component: ScanDetailComponent },
  { path: 'viewer/:manga/:chapter', component: ChapterViewerComponent }
];
