from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, URL


app = FastAPI()

@app.post("/parse")
def add_url(url: str):
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    db = SessionLocal()
    try:
        new_url = URL(link=url)
        db.add(new_url)
        db.commit()
        return {"message": "URL added successfully"}
    except IntegrityError:
        db.rollback() 
        raise HTTPException(status_code=400, detail="Duplicate URL")
    finally:
        db.close()

@app.get("/ads")
def get_urls():
    db = SessionLocal()
    try:
        urls = db.query(URL).all()
        return [{"id": url.id, "link": url.link} for url in urls]
    finally:
        db.close()
