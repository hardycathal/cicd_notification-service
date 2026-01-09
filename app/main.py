from fastapi import FastAPI, Depends, HTTPException, status, Response
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import select

from .database import engine, get_db
from .models import Base, NotificationDB
from .schemas import NotificationCreate, NotificationRead

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Notification Service", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/notifications", response_model=list[NotificationRead])
def list_notifications(db: Session = Depends(get_db)):
    stmt = select(NotificationDB).order_by(NotificationDB.id.desc())
    return db.execute(stmt).scalars().all()

@app.post("/api/notifications", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def create_notification(payload: NotificationCreate, db: Session = Depends(get_db)):
    n = NotificationDB(**payload.model_dump())
    db.add(n)
    db.commit()
    db.refresh(n)
    return n

@app.get("/api/notifications/{notif_id}", response_model=NotificationRead)
def get_notification(notif_id: int, db: Session = Depends(get_db)):
    n = db.get(NotificationDB, notif_id)
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    return n

@app.delete("/api/notifications/{notif_id}", status_code=204)
def delete_notification(notif_id: int, db: Session = Depends(get_db)) -> Response:
    n = db.get(NotificationDB, notif_id)
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(n)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
