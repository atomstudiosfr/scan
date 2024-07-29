import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';

@Component({
    selector: 'app-footer',
    standalone: true,
    imports: [CommonModule],
    template: `
        <footer>
            <div class="footer-content">
                <p>&copy; {{ currentYear }} ScanViewer. All rights reserved.</p>
            </div>
        </footer>
    `,
    styles: [`
        footer {
            background: #000000;
            color: #fff;
            text-align: center;
            padding: 0.4em 0;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    `]
})
export class FooterComponent {
    currentYear: number = new Date().getFullYear();
}
