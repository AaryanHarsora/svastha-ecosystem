import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.database import get_db
from db import queries
from schemas.order import OrderCreate, OrderStatusUpdate
from schemas.inventory import InventoryUpdate

router = APIRouter()

@router.get("/inventory")
def inventory_summary(db: Session = Depends(get_db)):
    return dict(queries.get_inventory_summary(db))

@router.get("/stock")
def stock_availability(db: Session = Depends(get_db)):
    result = queries.get_stock_availability(db)
    return {"stock": [dict(r) for r in result]}

@router.get("/vendors")
def vendor_list(db: Session = Depends(get_db)):
    result = queries.get_vendor_supply_list(db)
    return {"vendors": [dict(r) for r in result]}

@router.get("/orders/summary")
def orders_summary(db: Session = Depends(get_db)):
    return dict(queries.get_total_order_value(db))

@router.get("/orders/per-patient")
def orders_per_patient(db: Session = Depends(get_db)):
    result = queries.get_orders_per_patient(db)
    return {"patients": [dict(r) for r in result]}

@router.post("/orders", status_code=201)
def create_order(body: OrderCreate, db: Session = Depends(get_db)):
    oid = str(uuid.uuid4())
    total = 0.0
    for item in body.items:
        row = db.execute(text("SELECT price, stock FROM Inventory WHERE inventory_id = :iid"),
                         {"iid": item.inventory_id}).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail=f"Inventory item {item.inventory_id} not found")
        if row["stock"] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {item.inventory_id}")
        total += float(row["price"]) * item.quantity

    db.execute(text("""
        INSERT INTO Orders (order_id, patient_id, total_amount)
        VALUES (:oid, :patient_id, :total)
    """), {"oid": oid, "patient_id": body.patient_id, "total": total})

    for item in body.items:
        price = db.execute(text("SELECT price FROM Inventory WHERE inventory_id = :iid"),
                           {"iid": item.inventory_id}).scalar()
        db.execute(text("""
            INSERT INTO Order_Items (item_id, order_id, inventory_id, quantity, unit_price)
            VALUES (:iid, :oid, :inv_id, :qty, :price)
        """), {"iid": str(uuid.uuid4()), "oid": oid,
               "inv_id": item.inventory_id, "qty": item.quantity, "price": price})
        db.execute(text("UPDATE Inventory SET stock = stock - :qty WHERE inventory_id = :iid"),
                   {"qty": item.quantity, "iid": item.inventory_id})

    db.commit()
    return {"message": "Order placed", "order_id": oid, "total_amount": total}

@router.put("/orders/{order_id}/status")
def update_order_status(order_id: str, body: OrderStatusUpdate, db: Session = Depends(get_db)):
    result = db.execute(text("UPDATE Orders SET status = :status WHERE order_id = :oid"),
                        {"status": body.status, "oid": order_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated"}

@router.delete("/orders/{order_id}")
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    result = db.execute(text("UPDATE Orders SET status = 'Cancelled' WHERE order_id = :oid"),
                        {"oid": order_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order cancelled"}

@router.put("/inventory/{inventory_id}")
def update_inventory(inventory_id: str, body: InventoryUpdate, db: Session = Depends(get_db)):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["iid"] = inventory_id
    result = db.execute(text(f"UPDATE Inventory SET {set_clause} WHERE inventory_id = :iid"), fields)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return {"message": "Inventory updated"}