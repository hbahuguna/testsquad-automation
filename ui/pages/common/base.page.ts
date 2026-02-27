import { Page } from '@playwright/test';

export class BasePage {
    constructor(protected page: Page) { }

    async goto(path = '/') {
        await this.page.goto(path);
    }

    async getTitle() {
        return await this.page.title();
    }
}
