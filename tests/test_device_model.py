# test_device_model.py
import unittest
from app import app, db, Device
from test_config import TestConfig

class DeviceModelTestCase(unittest.TestCase):
    """
    A test case for the Device model in the Flask application.
    """

    def setUp(self):
        """
        Set up the test client and initialize the database before each test.
        """
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Remove the database session and drop all tables after each test.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_device(self):
        """
        Test creating a new device in the database.
        """
        with app.app_context():
            new_device = Device(
                device_name="Test Device",
                device_type="Agent",
                status="Online",
                ip_address="192.168.1.1"
            )
            db.session.add(new_device)
            db.session.commit()
            self.assertIsNotNone(new_device.id)
            self.assertEqual(new_device.device_name, "Test Device")
            print(f"Created device with ID: {new_device.id}")

    def test_read_device(self):
        """
        Test reading a device from the database.
        """
        with app.app_context():
            new_device = Device(
                device_name="Test Device",
                device_type="Agent",
                status="Online",
                ip_address="192.168.1.1"
            )
            db.session.add(new_device)
            db.session.commit()
            device = Device.query.filter_by(device_name="Test Device").first()
            self.assertIsNotNone(device)
            self.assertEqual(device.device_name, "Test Device")
            print(f"Read device with ID: {device.id}")

    def test_update_device(self):
        """
        Test updating a device in the database.
        """
        with app.app_context():
            new_device = Device(
                device_name="Test Device",
                device_type="Agent",
                status="Online",
                ip_address="192.168.1.1"
            )
            db.session.add(new_device)
            db.session.commit()
            device = Device.query.filter_by(device_name="Test Device").first()
            self.assertIsNotNone(device)
            device.status = "Offline"
            db.session.commit()
            updated_device = Device.query.filter_by(device_name="Test Device").first()
            self.assertEqual(updated_device.status, "Offline")
            print(f"Updated device with ID: {updated_device.id}")

    def test_delete_device(self):
        """
        Test deleting a device from the database.
        """
        with app.app_context():
            new_device = Device(
                device_name="Test Device",
                device_type="Agent",
                status="Online",
                ip_address="192.168.1.1"
            )
            db.session.add(new_device)
            db.session.commit()
            device = Device.query.filter_by(device_name="Test Device").first()
            self.assertIsNotNone(device)
            db.session.delete(device)
            db.session.commit()
            deleted_device = Device.query.filter_by(device_name="Test Device").first()
            self.assertIsNone(deleted_device)
            print("Deleted device successfully")

if __name__ == '__main__':
    unittest.main()
