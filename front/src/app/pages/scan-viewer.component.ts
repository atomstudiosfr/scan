import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ScanListComponent} from './scan-list.component';
import {ScanDetailsComponent} from './scan-details.component';
import {ScanReaderComponent} from './scan-reader.component';

@Component({
    selector: 'app-scan-viewer',
    standalone: true,
    imports: [CommonModule, ScanListComponent, ScanDetailsComponent, ScanReaderComponent],
    template: `
        <div class="scan-viewer">
            <app-scan-list></app-scan-list>
            <app-scan-details></app-scan-details>
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
