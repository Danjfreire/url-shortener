import unittest
from unittest.mock import patch
import datetime
from url_repo import UrlRepo
from pydantic import HttpUrl

class TestUnitRepo(unittest.TestCase):

    # This is run before any test
    @classmethod
    def setUpClass(cls):
        cls.repo = UrlRepo()
        cls.test_url = HttpUrl("https://example.com")
        cls.test_code = "code123"
    
    # This is run before each test - beforeEach
    def setUp(self):
        self.repo.url_db.clear()
        self.repo.code_db.clear()
        self.repo.stats_db.clear()
    
    # This is run after each test - afterEach
    def tearDown(self):
        pass


    @patch('url_repo.datetime')
    def test_save_shortened_url(self, mock_datetime):
        fake_time = datetime.datetime(2025, 1, 7, 12, 0, 0)
        mock_datetime.datetime.now.return_value = fake_time

        res = self.repo.save_shortened_url(self.test_url, self.test_code)

        self.assertEqual(res.code, self.test_code)
        self.assertEqual(res.url, self.test_url)
        self.assertEqual(res.created_at, fake_time)
        self.assertEqual(res.updated_at, fake_time)
    

    def test_find_by_original_url(self):
        res1 = self.repo.find_by_original_url(self.test_url)
        self.repo.save_shortened_url(self.test_url, self.test_code)
        res2 = self.repo.find_by_original_url(self.test_url)

        self.assertEqual(res1, None)
        self.assertEqual(res2.code, self.test_code)
        self.assertEqual(res2.url, self.test_url)

    def test_find_by_code(self):
        res1 = self.repo.find_by_code(self.test_code)
        self.repo.save_shortened_url(self.test_url, self.test_code)
        res2 = self.repo.find_by_code(self.test_code)

        self.assertEqual(res1, None)
        self.assertEqual(res2.code, self.test_code)
        self.assertEqual(res2.url, self.test_url)
    
    @patch("url_repo.datetime")
    def test_update_shortened_url(self, mock_datetime):
        fake_creation_time = datetime.datetime(2025, 1, 7, 12, 0, 0)
        mock_datetime.datetime.now.return_value = fake_creation_time 
        short_url = self.repo.save_shortened_url(self.test_url, self.test_code)
        fake_update_time = datetime.datetime(2025, 1, 7, 14, 0, 0)
        mock_datetime.datetime.now.return_value = fake_update_time
        new_url = HttpUrl("https://newurl.com")
        res = self.repo.update_shortened_url(short_url, new_url)

        self.assertEqual(self.repo.url_db[new_url], res)
        self.assertEqual(self.repo.code_db[res.code], res)
        self.assertEqual(res.url, new_url)
        self.assertEqual(res.code, self.test_code)
        self.assertEqual(res.created_at, fake_creation_time)
        self.assertEqual(res.updated_at, fake_update_time)
    
    def test_delete_shortened_url(self):
        short_url = self.repo.save_shortened_url(self.test_url, self.test_code)

        self.assertEqual(self.repo.url_db.get(self.test_url, None), short_url)
        self.assertEqual(self.repo.code_db.get(self.test_code), short_url)

        self.repo.delete_shortened_url(short_url)

        self.assertEqual(self.repo.url_db.get(self.test_url, None), None)
        self.assertEqual(self.repo.code_db.get(self.test_code), None)
    
    def test_increase_stats(self):
        short_url = self.repo.save_shortened_url(self.test_url, self.test_code)

        self.repo.increase_stats(short_url.code)
        self.repo.increase_stats(short_url.code)
        self.repo.increase_stats(short_url.code)

        short_url_stats = self.repo.find_shortened_url_stats(short_url)

        self.assertEqual(short_url_stats.code, self.test_code)
        self.assertEqual(short_url_stats.url, self.test_url)
        self.assertEqual(short_url_stats.created_at, short_url.created_at)
        self.assertEqual(short_url_stats.updated_at, short_url.updated_at)
        self.assertEqual(short_url_stats.access_count, 3)


        





if __name__ == "__main__":
    unittest.main()
