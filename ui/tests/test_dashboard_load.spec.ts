import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('TestSquad E2E Dashboard Validations', () => {

    test('should redirect unauthenticated users to the NextAuth login page', async ({ page }) => {
        // 1. Navigate to the frontend dashboard 
        await page.goto(BASE_URL);

        // 2. NextAuth middleware should intercept and redirect to custom login page
        await expect(page).toHaveURL(/.*login.*/);

        // 3. Assert the default NextAuth sign-in elements are present
        await expect(page.getByRole('button', { name: /Sign in with Google/i })).toBeVisible();
    });

    // NOTE: The fully authenticated dashboard flow requires injecting a valid JWE NextAuth token
    // into the Playwright browser context. For the purpose of this initial pipeline verification,
    // we ensure the frontend is up and properly secured.
    test.skip('should verify the chat console is fully interactive (requires auth bypass)', async ({ page }) => {
        await page.goto(BASE_URL);
        const chatInput = page.getByPlaceholder(/Type a message/i);
        await expect(chatInput).toBeVisible();
    });
});
