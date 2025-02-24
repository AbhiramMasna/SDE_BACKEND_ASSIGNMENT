from celery import Celery
import requests
from PIL import Image
from io import BytesIO
import uuid
from database import SessionLocal
from models import ImageModel, RequestModel

celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery.task
def process_images(request_id: str):
    db = SessionLocal()
    images = db.query(ImageModel).filter_by(request_id=request_id, status="pending").all()

    for image in images:
        response = requests.get(image.input_url)
        img = Image.open(BytesIO(response.content))

        output_filename = f"compressed_{uuid.uuid4().hex}.jpg"
        img.save(output_filename, "JPEG", quality=50)  

        image.output_url = output_filename  # Replace with cloud storage URL in production
        image.status = "done"
        db.commit()

    request = db.query(RequestModel).filter_by(id=request_id).first()
    request.status = "completed"
    db.commit()
    db.close()
    return {"message": "Images processed"}
