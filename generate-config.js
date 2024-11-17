// generate-config.js
const fs = require('fs');
const path = require('path');

// Read the .env file content
const envContent = fs.readFileSync(path.join(__dirname, 'backend', '.env'), 'utf8');

// Parse the .env content
const envVars = {};
envContent.split('\n').forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) {
        envVars[key.trim()] = value.trim();
    }
});

// Create the config content
const configContent = `// This file is auto-generated - do not edit manually
const config = {
    ni_url: "http://127.0.0.1:${envVars.PORT_NI || 8002}",
    atm_url: "http://127.0.0.1:${envVars.PORT_ATM || 8001}",
    core_banking_url: "http://127.0.0.1:${envVars.PORT_BANKING || 8000}"
};

export default config;`;

// Write the config.js file
fs.writeFileSync(path.join(__dirname, 'frontend', 'config.js'), configContent);

console.log('Config file generated successfully!');