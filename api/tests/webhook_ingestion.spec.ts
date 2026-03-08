import { test, expect } from '@playwright/test';
import crypto from 'crypto';

test.describe('Epic 2: Webhook PR Ingestion', () => {

    test('should ingest a pull request webhook successfully', async ({ request }) => {
        // Mock a GitHub Pull Request Payload
        const payload = {
            action: 'opened',
            number: 32,
            pull_request: {
                id: 3335791563,
                number: 32,
                state: 'open',
                title: 'TestSquad E2E API Test PR',
                user: { login: 'skaparwan' },
                head: {
                    ref: 'e2e-api-test-branch',
                    sha: '1234567890abcdef1234567890abcdef12345678',
                    repo: {
                        full_name: 'hbahuguna/testsquad',
                        html_url: 'https://github.com/hbahuguna/testsquad'
                    }
                },
                base: {
                    ref: 'main',
                    sha: '0987654321fedcba0987654321fedcba09876543'
                }
            },
            repository: {
                full_name: 'hbahuguna/testsquad'
            }
        };

        const payloadString = JSON.stringify(payload);
        const secret = process.env.GITHUB_WEBHOOK_SECRET || 'your_development_webhook_secret';

        // Compute GitHub HMAC Signature
        const signature = `sha256=${crypto.createHmac('sha256', secret).update(payloadString).digest('hex')}`;

        // 1. Send the Webhook Request
        const response = await request.post('/api/webhooks/github', {
            data: payload,
            headers: {
                'X-GitHub-Event': 'pull_request',
                'X-Hub-Signature-256': signature,
                'Content-Type': 'application/json'
            }
        });

        // The webhook should be accepted or processed
        expect(response.ok()).toBeTruthy();
        const responseData = await response.json();
        expect(responseData.status).toBe('processed');

        // 2. Poll the Database/API to confirm the Activity was created
        // We will fetch the recent activities and look for this PR
        await expect.poll(async () => {
            const activitiesResponse = await request.get('/api/activities');
            expect(activitiesResponse.ok()).toBeTruthy();
            const data = await activitiesResponse.json();

            // Check if our mock PR is in the activities list
            const ourActivity = data.activities.find((a: any) => a.id === `github-pr_ingested-3335791563`);
            return ourActivity !== undefined;
        }, {
            message: 'Activity was not created within the timeout',
            timeout: 10000, // 10 seconds
        }).toBeTruthy();
    });
});
