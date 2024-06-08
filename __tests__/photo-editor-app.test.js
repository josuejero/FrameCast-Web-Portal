const puppeteer = require('puppeteer');

describe('Photo Editor App', () => {
    let browser;
    let page;

    beforeAll(async () => {
        browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
            executablePath: '/usr/bin/chromium-browser'  // Adjust this path if necessary
        });
        page = await browser.newPage();
    });

    beforeEach(async () => {
        // Ensure the initial state is clean before each test
        await page.goto('http://localhost:5000/reset'); // Endpoint to reset state
        await page.goto('http://localhost:5000/photo-editor');
    });

    afterAll(async () => {
        if (browser) {
            await browser.close();
        }
    });

    test('should fetch all photos on load', async () => {
        await page.waitForSelector('.photo-list');
        const photos = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('.photo-list label')).map(label => label.textContent.trim());
        });
        console.log('Fetched photos:', photos);
        expect(photos).toContain('Photo1');
        expect(photos).toContain('Photo2');
    });

    test('should upload a new photo', async () => {
        const initialPhotos = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('.photo-list label')).map(label => label.textContent.trim());
        });
        console.log('Initial photos:', initialPhotos);
        expect(initialPhotos).not.toContain('New Photo');

        // Click the upload button
        await page.click('.upload-button');
        console.log('Clicked upload button');

        // Wait for the simulated upload to complete
        await page.waitForSelector('.photo-list label');

        const photosAfterUpload = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('.photo-list label')).map(label => label.textContent.trim());
        });
        console.log('Photos after upload:', photosAfterUpload);
        expect(photosAfterUpload).toContain('New Photo');
    }, 240000); // Increase the timeout for this test to 240 seconds
});
