from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import Movement, Stock, Material, User
from schemas.movement import MovementCreate, MovementRead
from utils.enums import MovementType
from uuid import UUID


def create_movement(db: Session, data: MovementCreate, current_user: User) -> MovementRead:
    # ✅ Permissões
    if data.type_insertion in [MovementType.entry, MovementType.exit]:
        if current_user.role not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores e gerentes podem registrar entradas/saídas."
            )
    elif data.type_insertion == MovementType.adjustment:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem realizar ajustes."
            )

    # ✅ Material deve existir
    material = db.query(Material).filter(Material.id == data.item_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado."
        )

    # ✅ Estoque deve existir (foi criado na criação do material)
    stock = db.query(Stock).filter(Stock.material_id == material.id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Estoque inconsistente: material não possui registro de estoque."
        )

    # ✅ Regras de movimentação
    if data.type_insertion == MovementType.entry:
        stock.value += data.value
    elif data.type_insertion == MovementType.exit:
        if stock.value < data.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Saldo de estoque insuficiente para saída."
            )
        stock.value -= data.value
    elif data.type_insertion == MovementType.adjustment:
        stock.value = data.value

    # ✅ Criação da movimentação (usa *_id e não os relacionamentos)
    new_movement = Movement(
        description=data.description,
        value=data.value,
        type_insertion=data.type_insertion,
        item_id=material.id,
        insert_by=current_user.id
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    # ✅ Carregar os relacionamentos para retorno
    movement_full = (
        db.query(Movement)
        .options(joinedload(Movement.item), joinedload(Movement.inserted_by))
        .filter(Movement.id == new_movement.id)
        .first()
    )

    return MovementRead(
        id=movement_full.id,
        description=movement_full.description,
        value=movement_full.value,
        type_insertion=movement_full.type_insertion,
        item=movement_full.item.name,
        inserted_by=movement_full.inserted_by.full_name,
        created_at=movement_full.created_at
    )


def get_all_movements(db: Session) -> list[MovementRead]:
    movements = (
        db.query(Movement)
        .options(joinedload(Movement.inserted_by), joinedload(Movement.item))  
        .all()
    )

    return [
        MovementRead(
            id=m.id,
            description=m.description,
            item=m.item.name, 
            value=m.value,
            type_insertion=m.type_insertion,
            created_at=m.created_at,
            inserted_by=m.inserted_by.full_name
        )
        for m in movements
    ]