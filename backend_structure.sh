#!/bin/bash

# Set the base directory
BACKEND_DIR="fastapi-paper-fetcher"

# Create backend root directory
mkdir -p $BACKEND_DIR/app/apis
mkdir -p $BACKEND_DIR/app/output

# Create required files
touch $BACKEND_DIR/app/main.py
touch $BACKEND_DIR/app/models.py
touch $BACKEND_DIR/app/services.py
touch $BACKEND_DIR/app/utils.py
touch $BACKEND_DIR/app/__init__.py
touch $BACKEND_DIR/app/apis/__init__.py
touch $BACKEND_DIR/app/apis/arxiv.py
touch $BACKEND_DIR/app/apis/semantic_scholar.py
touch $BACKEND_DIR/app/apis/core_api.py
touch $BACKEND_DIR/app/apis/unpaywall.py
touch $BACKEND_DIR/app/apis/pypaperbot.py
touch $BACKEND_DIR/app/apis/combined.py

# Create requirements file and README
touch $BACKEND_DIR/requirements.txt
echo "fastapi\nuvicorn\nhttpx\nrequests" > $BACKEND_DIR/requirements.txt
touch $BACKEND_DIR/README.md

echo "Backend folder structure created successfully."
