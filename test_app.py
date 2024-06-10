# test_app.py
import unittest
from app import app, db, get_ip_address
from test_config import TestConfig

class FlaskTestCase(unittest.TestCase):
    """
    A test case for the Flask application.
    """

    def setUp(self):
        """
        Set up the test client and initialize the database before each test.
        """
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Remove the database session and drop all tables after each test.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_simulated_photo_config(self):
        """
        Test the simulated photo config API endpoint.
        """
        response = self.app.get('/api/simulated_photo_config')
        self.assertEqual(response.status_code, 200)
        self.assertIn('photo_id', response.json)

    def test_simulated_photos(self):
        """
        Test the simulated photos API endpoint.
        """
        response = self.app.get('/api/simulated_photos')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1', response.json)

    def test_get_ip_address(self):
        """
        Test the get_ip_address function.
        """
        ip_address, fqdn = get_ip_address()
        self.assertIsNotNone(ip_address)
        self.assertIsNotNone(fqdn)

    def test_find_discoverable_bluetooth_devices(self):
        """
        Test the find_discoverable_bluetooth_devices API endpoint.
        """
        response = self.app.get('/api/find_discoverable_bluetooth_devices')
        self.assertEqual(response.status_code, 200)
        self.assertIn("00:11:22:33:44:55", response.json)

    def test_upload_photo(self):
        """
        Test the upload_photo API endpoint.
        """
        new_photo = {"photo_name": "Test Photo", "path": "path/to/test_photo.jpg"}
        response = self.app.post('/api/upload_photo', json=new_photo)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])

if __name__ == '__main__':
    unittest.main()
