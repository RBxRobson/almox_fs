from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import Material, Category, User, Stock
from schemas.material import MaterialCreate, MaterialUpdate, MaterialRead
from uuid import UUID
from typing import List, Optional


def create_material(db: Session, data: MaterialCreate, current_user: User) -> MaterialRead:
    # 🔎 Verifica se já tem permissão para criar materiais
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar materiais."
        )

    # 🔎 Verifica se já existe material com mesmo nome
    existing_material = db.query(Material).filter(Material.name == data.name).first()
    if existing_material:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um material com o nome '{data.name}'."
        )

    category_name = data.category_name or "NA"

    # 🔎 Busca ou cria a categoria
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    # 🔹 Criação do material
    new_material = Material(
        name=data.name,
        created_by=current_user.id,
        category_id=category.id
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)

    # 🔹 Criação do estoque inicial (valor 0)
    stock = Stock(
        material_id=new_material.id,
        value=0
    )
    db.add(stock)
    db.commit()

    return MaterialRead(
        id=new_material.id,
        name=new_material.name,
        created_by=current_user.full_name,
        category=category.name,
        created_at=new_material.created_at
    )

def get_all_materials(
    db: Session, category: Optional[str] = None, name: Optional[str] = None
) -> List[MaterialRead]:
    query = (
        db.query(Material)
        .options(joinedload(Material.creator), joinedload(Material.category))
    )

    # Filtra por categoria (case insensitive)
    if category:
        query = query.filter(Material.category.has(name__ilike=f"%{category}%"))

    # Filtra por nome (case insensitive)
    if name:
        query = query.filter(Material.name.ilike(f"%{name}%"))

    materials = query.all()

    return [
        MaterialRead(
            id=m.id,
            name=m.name,
            created_by=m.creator.full_name if m.creator else "Desconhecido",
            category=m.category.name if m.category else "NA",
            created_at=m.created_at
        )
        for m in materials
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
        created_by=material.creator.full_name,
        category=material.category.name,
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
