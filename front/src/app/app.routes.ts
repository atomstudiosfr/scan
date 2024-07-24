import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home.component';
import { ScanViewerComponent } from './pages/scan-viewer.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'viewer', component: ScanViewerComponent },
];
