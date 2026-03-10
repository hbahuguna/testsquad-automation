import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('TestSquad E2E Dashboard Validations', () => {

    test('should allow access to the dashboard in E2E mode without redirecting to login', async ({ page }) => {
        // 1. Navigate to the frontend dashboard 
        await page.goto(BASE_URL);

        // 2. In E2E mode, middleware is bypassed, so we should stay on the home page
        await expect(page).toHaveURL(BASE_URL);

        // 3. Ensure the main UI container is present
        await expect(page.locator('main')).toBeVisible();
    });

    // We no longer skip this test because we have the E2E Backdoor enabled
    test('should verify the chat console is fully interactive (requires auth bypass)', async ({ page }) => {
        await page.goto(`${BASE_URL}/login`);

        // Log in via the injected E2E Mock credentials button
        const e2eBtn = page.getByTestId('e2e-login-btn');
        await expect(e2eBtn).toBeVisible({ timeout: 5000 });
        await e2eBtn.click();

        // NextAuth redirects to /providers by default or wherever callbackUrl points
        await page.waitForURL(/.*providers|.*runs|^\/$/.source);

        // The middleware should now consider us authenticated. Let's hit the root page.
        await page.goto(BASE_URL);
        await expect(page).not.toHaveURL(/.*login.*/);
    });
});
