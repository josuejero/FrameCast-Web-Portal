from app import app, db, Photo

# Ensure the app context is available
with app.app_context():
    # Create a new photo
    new_photo = Photo(photo_name="Test Photo", path="/path/to/test_photo.jpg")
    db.session.add(new_photo)
    db.session.commit()

    # Read the photo
    photo = Photo.query.first()
    print(f"Photo: {photo.photo_name}, Path: {photo.path}")

    # Update the photo
    photo.rotation = 90
    db.session.commit()
    updated_photo = Photo.query.first()
    print(f"Updated Photo Rotation: {updated_photo.rotation}")

    # Delete the photo
    db.session.delete(photo)
    db.session.commit()

    # Verify deletion
    deleted_photo = Photo.query.first()
    if deleted_photo is None:
        print("Photo deleted successfully")
    else:
        print("Photo deletion failed")
