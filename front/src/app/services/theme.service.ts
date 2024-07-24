import {Inject, Injectable} from '@angular/core';
import {DOCUMENT} from '@angular/common';

@Injectable({
    providedIn: 'root',
})
export class ThemeService {

    constructor(@Inject(DOCUMENT) private document: Document) {
    }

    switchTheme(theme: string) {
        let themeLink = this.document.getElementById('theme-css') as HTMLLinkElement;
        if (themeLink) {
            themeLink.href = `assets/styles/theme/lara-${theme}-purple/theme.css`;
        }
    }
}
