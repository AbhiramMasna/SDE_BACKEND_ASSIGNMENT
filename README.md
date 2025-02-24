Backend Assignment for spyne.ai
How it Works:
Upload API (/upload) – Accepts CSV, stores data in DB, and triggers async processing.
Status API (/status/{request_id}) – Checks processing status.
Asynchronous Image Processing (Celery Task) – Downloads and compresses images.
Database (SQLite/PostgreSQL) – Stores image processing details.
Next Steps:
Deploy Redis & Celery for async processing.
Use AWS S3/Cloudinary for storing images.
Implement Webhook (Bonus) for real-time updates.
