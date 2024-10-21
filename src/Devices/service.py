from datetime import datetime
from sqlmodel import Session
from typing import Optional, Any
from .models import UserDevices, UserDevicesCreate, UserDevicesRead


def upsert_user_device(db: Session, device_data: UserDevicesCreate) -> UserDevices | Any:
    # Check if the user device already exists based on device_id
    existing_device = db.query(UserDevices).filter(UserDevices.device_id == device_data.device_id).first()

    if existing_device:
        # Update the last_seen date
        existing_device.last_seen = datetime.now()
        db.commit()
        db.refresh(existing_device)

        return  {
            'status': 'true',
            'message': 'Device Updated successfully.',
            'data': existing_device
        }

    else:
        # Create a new device entry
        new_device = UserDevices(
            user_id=device_data.user_id,
            device_id=device_data.device_id,
            device_name=device_data.device_name,
            ip_address=device_data.ip_address,
            last_seen=datetime.now(),
            login_time=datetime.now()
        )
        db.add(new_device)
        db.commit()
        db.refresh(new_device)

        return {
            'status': 'true',
            'message': 'Device created successfully.',
            'data': new_device
        }

def delete_user_device(db: Session, device_id: str) -> dict:
    # Find the device to delete
    device_to_delete = db.query(UserDevices).filter(UserDevices.device_id == device_id).first()

    if not device_to_delete:
        return {
            'status': 'false',
            'message': 'Device not found.',
            'data': None
        }

    # Delete the device
    db.delete(device_to_delete)
    db.commit()

    return {
        'status': 'true',
        'message': 'Device deleted successfully.',
        'data': device_to_delete
    }


def get_user_devices(db: Session, user_id: int) -> dict:
    devices = db.query(UserDevices).filter(UserDevices.user_id == user_id).all()

    return {
        'status': 'true',
        'message': 'User devices retrieved successfully.',
        'data': devices
    }
