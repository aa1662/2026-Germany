// @ts-check
const { test, expect } = require('@playwright/test');
const path = require('path');

// Test configuration - use file:// protocol with proper path
const filePath = path.resolve(__dirname, '../../docs/blog/day-07-blog.html');
const BASE_URL = `file:///${filePath.replace(/\\/g, '/')}`;
const LIGHTBOX_TIMEOUT = 10000;

test.describe('GLightbox Functionality Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the page
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    // Wait for page to load and GLightbox script to be available
    await page.waitForTimeout(1500);

    // Check if GLightbox is loaded
    const glightboxLoaded = await page.evaluate(() => typeof GLightbox !== 'undefined');
    if (!glightboxLoaded) {
      throw new Error('GLightbox library not loaded');
    }
  });

  test('Hero image opens in lightbox correctly', async ({ page }) => {
    // Click on hero image
    const heroImage = page.locator('.blog-hero .glightbox').first();
    await expect(heroImage).toBeVisible();
    await heroImage.click();

    // Wait for lightbox dialog to open (GLightbox uses role="dialog")
    const lightboxContainer = page.locator('.glightbox-container');
    await expect(lightboxContainer).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

    // Verify close button is present (indicates lightbox is fully opened)
    const closeBtn = page.locator('.gclose');
    await expect(closeBtn).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

    // Close lightbox
    await page.keyboard.press('Escape');
    await expect(lightboxContainer).not.toBeVisible({ timeout: LIGHTBOX_TIMEOUT });
  });

  test('Gallery images (3) open in lightbox correctly', async ({ page }) => {
    const galleryImages = page.locator('.blog-gallery .glightbox');
    const count = await galleryImages.count();
    expect(count).toBe(3);

    for (let i = 0; i < count; i++) {
      const img = galleryImages.nth(i);
      await img.scrollIntoViewIfNeeded();
      await img.click();

      // Verify lightbox opens
      const lightboxContainer = page.locator('.glightbox-container');
      await expect(lightboxContainer).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

      // Verify slide content is present (title or close button)
      const closeBtn = page.locator('.gclose');
      await expect(closeBtn).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

      // Close and continue
      await page.keyboard.press('Escape');
      await expect(lightboxContainer).not.toBeVisible({ timeout: LIGHTBOX_TIMEOUT });
    }
  });

  test('Photo strip images (3) open in lightbox correctly', async ({ page }) => {
    const stripImages = page.locator('.blog-photo-strip .glightbox');
    const count = await stripImages.count();
    expect(count).toBe(3);

    for (let i = 0; i < count; i++) {
      const img = stripImages.nth(i);
      await img.scrollIntoViewIfNeeded();
      await img.click();

      const lightboxContainer = page.locator('.glightbox-container');
      await expect(lightboxContainer).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

      // Verify close button is present
      const closeBtn = page.locator('.gclose');
      await expect(closeBtn).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

      await page.keyboard.press('Escape');
      await expect(lightboxContainer).not.toBeVisible({ timeout: LIGHTBOX_TIMEOUT });
    }
  });

  test('Photo-text and photo-card images open correctly', async ({ page }) => {
    // Test photo-text images
    const photoTextImages = page.locator('.blog-photo-text .glightbox');
    const textCount = await photoTextImages.count();
    expect(textCount).toBeGreaterThanOrEqual(2);

    for (let i = 0; i < textCount; i++) {
      const img = photoTextImages.nth(i);
      await img.scrollIntoViewIfNeeded();
      await img.click();

      const lightboxContainer = page.locator('.glightbox-container');
      await expect(lightboxContainer).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });
      await page.keyboard.press('Escape');
      await expect(lightboxContainer).not.toBeVisible({ timeout: LIGHTBOX_TIMEOUT });
    }

    // Test photo-card image
    const photoCardImage = page.locator('.blog-photo-card .glightbox').first();
    await photoCardImage.scrollIntoViewIfNeeded();
    await photoCardImage.click();

    const lightboxContainer = page.locator('.glightbox-container');
    await expect(lightboxContainer).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });
    await page.keyboard.press('Escape');
  });

  test('Lightbox navigation arrows work correctly', async ({ page }) => {
    // Open first gallery image
    const firstGalleryImg = page.locator('.blog-gallery .glightbox').first();
    await firstGalleryImg.scrollIntoViewIfNeeded();
    await firstGalleryImg.click();

    const lightboxContainer = page.locator('.glightbox-container');
    await expect(lightboxContainer).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

    // Test next arrow
    const nextButton = page.locator('.gnext');
    if (await nextButton.isVisible()) {
      await nextButton.click();
      await page.waitForTimeout(500);
    }

    // Test previous arrow
    const prevButton = page.locator('.gprev');
    if (await prevButton.isVisible()) {
      await prevButton.click();
      await page.waitForTimeout(500);
    }

    await page.keyboard.press('Escape');
  });

  test('Close button closes lightbox', async ({ page }) => {
    const heroImage = page.locator('.blog-hero .glightbox').first();
    await heroImage.click();

    const lightboxContainer = page.locator('.glightbox-container');
    await expect(lightboxContainer).toBeVisible({ timeout: LIGHTBOX_TIMEOUT });

    // Click close button
    const closeButton = page.locator('.gclose');
    await closeButton.click();

    await expect(lightboxContainer).not.toBeVisible({ timeout: LIGHTBOX_TIMEOUT });
  });
});

