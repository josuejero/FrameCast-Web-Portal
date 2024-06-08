import unittest
from app import app, db, get_ip_address

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_simulated_photo_config(self):
        response = self.app.get('/api/simulated_photo_config')
        self.assertEqual(response.status_code, 200)
        self.assertIn('photo_id', response.json)

    def test_simulated_photos(self):
        response = self.app.get('/api/simulated_photos')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1', response.json)

    def test_get_ip_address(self):
        ip_address, fqdn = get_ip_address()
        self.assertIsNotNone(ip_address)
        self.assertIsNotNone(fqdn)

    def test_map_url(self):
        response = self.app.get('/api/map_url')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])

if __name__ == '__main__':
    unittest.main()
