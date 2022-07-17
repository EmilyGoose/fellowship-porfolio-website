# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        # Make sure request returns 200
        response = self.client.get("/")
        assert response.status_code == 200
        
        # Make sure content is properly returned
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0


