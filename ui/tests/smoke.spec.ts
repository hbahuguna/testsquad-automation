import { test, expect } from '@playwright/test';

test('Smoke: Load Dashboard', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Create Next App/);
});
