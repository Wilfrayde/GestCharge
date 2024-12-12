from sqlalchemy.orm import Session
from .models import Material
from datetime import datetime

def add_material(session: Session, **kwargs):
    new_material = Material(**kwargs)
    session.add(new_material)
    session.commit()

def delete_material(session: Session, material_id: int):
    material = session.query(Material).get(material_id)
    if material:
        session.delete(material)
        session.commit()

def update_material(session: Session, material_id: int, **kwargs):
    # Filtrer les kwargs vides pour éviter les mises à jour inutiles
    valid_kwargs = {k: v for k, v in kwargs.items() if v is not None}
    if not valid_kwargs:
        return
    
    material = session.query(Material).get(material_id)
    if material:
        for key, value in valid_kwargs.items():
            setattr(material, key, value)
        session.commit()
