const { execSync } = require('child_process');

// Start XVFB before running the tests
execSync('Xvfb :99 -screen 0 1024x768x24 &', { stdio: 'inherit' });
process.env.DISPLAY = ':99';
