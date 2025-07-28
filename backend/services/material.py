from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import Material, Category, User
from schemas.material import MaterialCreate, MaterialUpdate, MaterialRead
from uuid import UUID
from typing import List


def create_material(db: Session, data: MaterialCreate, current_user: User) -> MaterialRead:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar materiais."
        )

    existing_material = db.query(Material).filter(Material.name == data.name).first()
    if existing_material:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um material com o nome '{data.name}'."
        )

    category_name = data.category_name or "NA"

    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    new_material = Material(
        name=data.name,
        created_by=current_user.id,
        category_id=category.id
    )

    db.add(new_material)
    db.commit()
    db.refresh(new_material)

    return MaterialRead(
        id=new_material.id,
        name=new_material.name,
        created_by=current_user.full_name,
        category=category.name,
        created_at=new_material.created_at
    )


def get_all_materials(db: Session) -> List[MaterialRead]:
    materials = (
        db.query(Material)
        .options(joinedload(Material.creator), joinedload(Material.category))
        .all()
    )

    return [
        MaterialRead(
            id=mat.id,
            name=mat.name,
            created_by=mat.creator.full_name if mat.creator else "Desconhecido",
            category=mat.category.name if mat.category else "NA",
            created_at=mat.created_at
        )
        for mat in materials
    ]


def update_material(db: Session, material_id: UUID, data: MaterialUpdate) -> MaterialRead:
    material = db.query(Material).filter_by(id=material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado."
        )

    material.name = data.name
    db.commit()
    db.refresh(material)

    return MaterialRead(
        id=material.id,
        name=material.name,
        created_by=material.creator.full_name if material.creator else "Desconhecido",
        category=material.category.name if material.category else "NA",
        created_at=material.created_at
    )


def delete_material(db: Session, material_id: UUID):
    material = db.query(Material).filter_by(id=material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado."
        )
    db.delete(material)
    db.commit()
