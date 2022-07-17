#!/bin/bash

# Make sure site is up to date from VCS
git fetch && git reset origin/main --hard

# Spin existing containers down
docker compose -f docker-compose.prod.yml down

# Build & spin up site
docker compose -f docker-compose.prod.yml up -d --build
