from sqlalchemy.orm import Session, joinedload
from models import Stock
from schemas.stock import StockRead
from typing import List, Optional


def get_all_stock(
    db: Session, category: Optional[str] = None, name: Optional[str] = None
) -> List[StockRead]:
    query = (
        db.query(Stock)
        .options(joinedload(Stock.material).joinedload("category"))
    )

    # Filtra por categoria
    if category:
        query = query.filter(Stock.material.has(category.has(name__ilike=f"%{category}%")))

    # Filtra por nome
    if name:
        query = query.filter(Stock.material.has(name.ilike(f"%{name}%")))

    stock_items = query.all()

    return [
        StockRead(
            id=s.id,
            material=s.material.name if s.material else "Desconhecido",
            value=s.value,
            category=s.material.category.name if s.material and s.material.category else "NA"
        )
        for s in stock_items
    ]
