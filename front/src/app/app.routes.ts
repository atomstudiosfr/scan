import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home.component';
import {ScanDetailComponent} from './pages/scan-detail.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'viewer/:title', component: ScanDetailComponent }
];
