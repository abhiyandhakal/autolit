#!/bin/bash

# Set the base directory
FRONTEND_DIR="react-paper-fetcher"

# Create frontend root directories
mkdir -p $FRONTEND_DIR/public
mkdir -p $FRONTEND_DIR/src/components
mkdir -p $FRONTEND_DIR/src/pages
mkdir -p $FRONTEND_DIR/src/api

# Create required files
touch $FRONTEND_DIR/public/index.html
touch $FRONTEND_DIR/src/App.js
touch $FRONTEND_DIR/src/index.js
touch $FRONTEND_DIR/src/components/SearchForm.jsx
touch $FRONTEND_DIR/src/components/ResultsDisplay.jsx
touch $FRONTEND_DIR/src/components/DownloadOption.jsx
touch $FRONTEND_DIR/src/pages/Home.jsx
touch $FRONTEND_DIR/src/pages/Results.jsx
touch $FRONTEND_DIR/src/api/apiClient.js

# Create package.json and README
touch $FRONTEND_DIR/package.json
cat <<EOL > $FRONTEND_DIR/package.json
{
  "name": "react-paper-fetcher",
  "version": "1.0.0",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "dependencies": {
    "axios": "^1.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-router-dom": "^6.0.0"
  }
}
EOL
touch $FRONTEND_DIR/README.md

echo "Frontend folder structure created successfully."
