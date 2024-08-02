const puppeteer = require('puppeteer');

describe('Photo Editor App', () => {
    let browser;
    let page;

    // Before all tests, launch the browser and create a new page
    beforeAll(async () => {
        browser = await puppeteer.launch({
            headless: true, // Run in headless mode
            args: ['--no-sandbox', '--disable-setuid-sandbox'], // Required for some environments
            executablePath: '/usr/bin/chromium-browser'  // Adjust this path if necessary
        });
        page = await browser.newPage();
    });

    // Before each test, reset the state and navigate to the photo editor page
    beforeEach(async () => {
        await page.goto('http://localhost:5000/reset'); // Endpoint to reset state
        await page.goto('http://localhost:5000/photo-editor'); // Navigate to the photo editor
    });

    // After all tests, close the browser
    afterAll(async () => {
        if (browser) {
            await browser.close();
        }
    });

    // Test to check if all photos are fetched on load
    test('should fetch all photos on load', async () => {
        await page.waitForSelector('.photo-list'); // Wait for the photo list to be rendered
        const photos = await page.evaluate(() => {
            // Extract the text content of each photo label
            return Array.from(document.querySelectorAll('.photo-list label')).map(label => label.textContent.trim());
        });
        console.log('Fetched photos:', photos);
        expect(photos).toContain('Photo1');
        expect(photos).toContain('Photo2');
    });

    // Test to check if a new photo can be uploaded
    test('should upload a new photo', async () => {
        // Get the initial list of photos
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

        // Get the updated list of photos
        const photosAfterUpload = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('.photo-list label')).map(label => label.textContent.trim());
        });
        console.log('Photos after upload:', photosAfterUpload);
        expect(photosAfterUpload).toContain('New Photo');
    }, 240000); // Increase the timeout for this test to 240 seconds
});
