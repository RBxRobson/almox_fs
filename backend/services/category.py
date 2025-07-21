from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.category import Category
from models.user import User, UserRole
from schemas.category import CategoryCreate


def get_by_name(db: Session, name: str) -> Optional[Category]:
    return db.query(Category).filter(Category.name == name).first()


def get_by_id(db: Session, category_id: UUID) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(
    db: Session,
    category_data: CategoryCreate,
    current_user: User
) -> Category:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar categorias."
        )

    existing = get_by_name(db, category_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria '{category_data.name}' já existe."
        )

    new_category = Category(
        name=category_data.name,
        created_by=current_user.id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_all_categories(db: Session):
    result = (
        db.query(
            Category.id,
            Category.name,
            Category.created_at,
            User.full_name.label("created_by")
        )
        .join(User, Category.created_by == User.id)
        .order_by(Category.name)
        .all()
    )

    # Converter resultado para dicionários
    return [
        {
            "id": row.id,
            "name": row.name,
            "created_at": row.created_at,
            "created_by": row.created_by,
        }
        for row in result
    ]
