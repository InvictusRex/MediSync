from sqlalchemy.orm import Session
from sqlalchemy import or_
import models

def verify_admin(db: Session, identifier: str, password: str):
    admin = db.query(models.Admin).filter(
        or_(
            models.Admin.email == identifier,
            models.Admin.phone == identifier
        )
    ).first()
    
    if admin and admin.verify_password(password):
        return admin
    return None