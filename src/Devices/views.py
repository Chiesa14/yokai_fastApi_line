from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.database import get_db
from .models import UserDevicesCreate, UserDevicesRead,UserDevices
from .service import upsert_user_device, delete_user_device, get_user_devices

router = APIRouter()

@router.post("/create-or-update-device")
def create_or_update_device(device_data: UserDevicesCreate, db: Session = Depends(get_db)):
    return upsert_user_device(db=db, device_data=device_data)

@router.delete("/delete-device/{device_id}")
def remove_device(device_id: str, db: Session = Depends(get_db)):
    return delete_user_device(db=db, device_id=device_id)

@router.get("/get-user-devices/{user_id}")
def retrieve_user_devices(user_id: int, db: Session = Depends(get_db)):

    return get_user_devices(db=db, user_id=user_id)

@router.get("/get-all-devices")
def retrieve_all_devices(db: Session = Depends(get_db)):

    devices = db.query(UserDevices).all()
    return {
        'status': 'true',
        'message': 'All devices retrieved successfully.',
        'data': devices
    }
