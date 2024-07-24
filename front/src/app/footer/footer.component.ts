import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  template: `
    <footer>
      <div class="footer-content">
        <p>&copy; 2023 ScanViewer. All rights reserved.</p>
      </div>
    </footer>
  `,
  styles: [`
    footer {
      background: #007ad9;
      color: #fff;
      text-align: center;
      padding: 1em 0;
      position: fixed;
      bottom: 0;
      width: 100%;
    }
  `]
})
export class FooterComponent {}
