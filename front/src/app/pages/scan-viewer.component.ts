import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ScanListComponent} from './scan-list.component';
import {ScanDetailComponent} from './scan-detail.component';
import {ScanReaderComponent} from './scan-reader.component';

@Component({
    selector: 'app-scan-viewer',
    standalone: true,
    imports: [CommonModule, ScanListComponent, ScanDetailComponent, ScanReaderComponent],
    template: `
        <div class="scan-viewer">
            <app-scan-list></app-scan-list>
            <app-scan-detail></app-scan-detail>
            <app-scan-reader></app-scan-reader>
        </div>
    `,
    styles: [`
        .scan-viewer {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1em;
        }
    `]
})
export class ScanViewerComponent {
}
