#!/bin/bash

# Test POST endpoint
curl -X POST http://localhost:5000/api/timeline_post -d 'name=Emily&email=emily@example.com&content=Test post'

# Test GET endpoint
curl http://localhost:5000/api/timeline_post
