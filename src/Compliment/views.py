from fastapi import Body, FastAPI, Depends,HTTPException,APIRouter
from sqlmodel import Session
from .models import CreateCompliment
from .service import (
    create_compliment,
    get_compliments,
    get_compliment_by_id,
    send_compliment
)
from src.database import get_db


router= APIRouter()

@router.post("/create/")
def create_compliment_endpoint(compliment: CreateCompliment, db: Session = Depends(get_db)):
    return create_compliment(db, compliment)

@router.get("/all")
def read_compliments(db:Session = Depends(get_db)):
    return  get_compliments(db)


@router.get("/{compliment_id}")
def read_compliment_by_id(compliment_id:int,db:Session= Depends(get_db)):
    compliment=get_compliment_by_id(db,compliment_id)
    if not compliment:
        raise HTTPException(status_code=404, detail="Compliment not found")
    return compliment


@router.post("/send-compliment/")
async def send_compliment_endpoint(
     sender_id: str = Body(...), 
    recipient_id: str = Body(...), 
    compliment_id: int = Body(...), 
    db: Session = Depends(get_db)):
  
    print("compliment_id: ",compliment_id)
    compliment = get_compliment_by_id(db, compliment_id)
    print(compliment)
    if not compliment:
        raise HTTPException(status_code=404, detail="Compliment not found")

    try:
        sent_compliment = await send_compliment(sender_id, recipient_id)
        return {"status": "success", "message": "Compliment sent successfully", "data": sent_compliment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send compliment: {str(e)}")