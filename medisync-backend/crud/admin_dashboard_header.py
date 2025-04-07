from sqlalchemy.orm import Session
from models import Admin
from schemas import AdminHeaderResponse

def get_admin_header_info(db: Session, admin_id: int) -> AdminHeaderResponse:
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        return None  # or raise an exception

    return AdminHeaderResponse(
        name=admin.name,
        admin_id=f"Admin ID: A{admin.id:05d}"  # Final format
    )
