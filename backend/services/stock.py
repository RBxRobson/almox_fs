from sqlalchemy.orm import Session, joinedload
from models import Stock, Material
from schemas.stock import StockRead
from typing import List


def get_all_stocks(db: Session) -> List[StockRead]:
    stocks = (
        db.query(Stock)
        .options(joinedload(Stock.material))
        .all()
    )

    return [
        StockRead(
            material_id=stock.material.id,
            material_name=stock.material.name,
            value=stock.value
        )
        for stock in stocks
    ]
