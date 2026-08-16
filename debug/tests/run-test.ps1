# GLightbox Test Runner Script
# This script runs Playwright tests for GLightbox functionality

Write-Host "================================" -ForegroundColor Cyan
Write-Host "GLightbox Test Runner" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
$nodeVersion = node --version 2>$null
if (-not $nodeVersion) {
    Write-Host "ERROR: Node.js is not installed" -ForegroundColor Red
    exit 1
}
Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green

# Check if Playwright is installed
$playwrightInstalled = npm list @playwright/test 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Playwright not found. Installing..." -ForegroundColor Yellow
    npm install @playwright/test
    npx playwright install chromium
}

# Run the tests
Write-Host ""
Write-Host "Running GLightbox tests..." -ForegroundColor Cyan
Write-Host ""

npx playwright test test-glightbox.spec.js --reporter=list

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Green
Write-Host "To see HTML report, run: npx playwright show-report" -ForegroundColor Cyan

