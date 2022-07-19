# test_db.py
# Unit test for the database

import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

# Create in-memory sqlite db for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind models to test db
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)

    def test_timeline_post(self):
        # Create 2 timeline posts and get IDs
        first_post = TimelinePost.create(name='test1', email='test1@example.com', content='Hello, world! Test #1')
        assert first_post.id == 1
        
        second_post = TimelinePost.create(name='test2', email='test2@example.com', content='Hello, World! Test #2')
        assert second_post.id == 2

