from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends
import pandas as pd
import uuid
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import RequestModel, ImageModel
from worker import process_images

app = FastAPI()

Base.metadata.create_all(bind=engine)  # Ensure tables exist

@app.post("/upload")
def upload_csv(file: UploadFile = File(...), background_tasks: BackgroundTasks = None, db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    request_id = str(uuid.uuid4())

    db.add(RequestModel(id=request_id, status="processing"))
    db.commit()

    for _, row in df.iterrows():
        product_name = row["Product Name"]
        input_urls = row["Input Image Urls"].split(",")
        for url in input_urls:
            db.add(ImageModel(request_id=request_id, product_name=product_name, input_url=url, status="pending"))
    
    db.commit()
    background_tasks.add_task(process_images, request_id)
    return {"request_id": request_id}

@app.get("/status/{request_id}")
def get_status(request_id: str, db: Session = Depends(get_db)):
    request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not request:
        return {"error": "Invalid request ID"}
    return {"request_id": request_id, "status": request.status}
