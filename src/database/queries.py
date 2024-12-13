from sqlalchemy.orm import Session
from .models import Material
from datetime import datetime

def add_material(session: Session, **kwargs):
    material = Material(**kwargs)
    session.add(material)
    return material

def delete_material(session: Session, material_id: int):
    material = session.query(Material).get(material_id)
    if material:
        session.delete(material)
    return True

def update_material_field(session: Session, material_id: int, field_name: str, new_value: any):
    material = session.query(Material).get(material_id)
    if material:
        setattr(material, field_name, new_value)
    return material
