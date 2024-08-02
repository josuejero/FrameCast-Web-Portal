# test_app.py
import unittest
from app import app, db, Photo
from test_config import TestConfig

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_save_photo_config(self):
        # Add a test photo
        with app.app_context():
            new_photo = Photo(photo_name="Test Photo", path="path/to/test_photo.jpg")
            db.session.add(new_photo)
            db.session.commit()
            photo_id = new_photo.id

        # Test saving photo config
        photo_config = {
            "photo_id": photo_id,
            "rotation": 90,
            "scaling": 50,
            "window": {"x": 10, "y": 20},
            "split_screen": {"x": 5, "y": 5, "width": 50, "height": 50}
        }
        response = self.app.post('/api/save_photo_config', json=photo_config)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])

        # Verify the photo config was saved
        with app.app_context():
            photo = Photo.query.get(photo_id)
            self.assertEqual(photo.rotation, 90)
            self.assertEqual(photo.scaling, 50)
            self.assertEqual(photo.window_x, 10)
            self.assertEqual(photo.window_y, 20)
            self.assertEqual(photo.split_screen_x, 5)
            self.assertEqual(photo.split_screen_y, 5)
            self.assertEqual(photo.split_screen_width, 50)
            self.assertEqual(photo.split_screen_height, 50)

if __name__ == '__main__':
    unittest.main()
