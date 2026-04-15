"""
queries.py
All 18 SQL demonstration queries for the Medical Recommendation
& Pharmacy Marketplace DBMS project.

Categories:
  1-2   Basic retrieval
  3-4   Filtering
  5-6   Joins
  7-9   Aggregation
  10-11 Grouping
  12    Subquery
  13-18 Additional / analytics
"""

from sqlalchemy import text
from sqlalchemy.orm import Session



# 1. BASIC — Retrieve all patients

def get_all_patients(db: Session):
    sql = text("""
        SELECT
            patient_id,
            name,
            age,
            gender,
            blood_group,
            phone,
            email
        FROM Patients
        ORDER BY name
    """)
    return db.execute(sql).mappings().all()



# 2. BASIC — Retrieve all medications

def get_all_medications(db: Session):
    sql = text("""
        SELECT
            medication_id,
            name,
            generic_name,
            category,
            dosage_form,
            strength
        FROM Medications
        ORDER BY category, name
    """)
    return db.execute(sql).mappings().all()



# 3. FILTER — Get risk score for a specific patient

def get_patient_risk_score(db: Session, patient_id: str):
    sql = text("""
        SELECT
            p.name,
            r.heart_score,
            r.cardio_score,
            r.kidney_score,
            r.overall_score,
            r.calculated_at
        FROM Risk_Scores r
        JOIN Patients p ON p.patient_id = r.patient_id
        WHERE r.patient_id = :patient_id
    """)
    return db.execute(sql, {"patient_id": patient_id}).mappings().first()



# 4. FILTER — High-risk patients (overall_score > 70)

def get_high_risk_patients(db: Session, threshold: float = 70.0):
    sql = text("""
        SELECT
            p.name,
            p.age,
            p.gender,
            r.heart_score,
            r.cardio_score,
            r.kidney_score,
            r.overall_score
        FROM Risk_Scores r
        JOIN Patients p ON p.patient_id = r.patient_id
        WHERE r.overall_score > :threshold
        ORDER BY r.overall_score DESC
    """)
    return db.execute(sql, {"threshold": threshold}).mappings().all()



# 5. JOIN — Recommended medicines for a patient
#    Patient → Patient_Diseases → Disease_Medications → Medications

def get_patient_recommendations(db: Session, patient_id: str):
    sql = text("""
        SELECT DISTINCT
            p.name                  AS patient_name,
            d.name                  AS disease_name,
            m.name                  AS medication_name,
            m.generic_name,
            m.category,
            m.dosage_form,
            m.strength
        FROM Patients p
        JOIN Patient_Diseases pd    ON p.patient_id   = pd.patient_id
        JOIN Diseases d             ON pd.disease_id  = d.disease_id
        JOIN Disease_Medications dm ON d.disease_id   = dm.disease_id
        JOIN Medications m          ON dm.medication_id = m.medication_id
        WHERE p.patient_id = :patient_id
        ORDER BY d.name, m.name
    """)
    return db.execute(sql, {"patient_id": patient_id}).mappings().all()



# 6. JOIN — Patient appointments with doctor and hospital

def get_patient_appointments(db: Session, patient_id: str):
    sql = text("""
        SELECT
            p.name                  AS patient_name,
            d.name                  AS doctor_name,
            d.specialization,
            h.name                  AS hospital_name,
            h.city,
            a.appointment_date,
            a.status,
            a.notes
        FROM Appointments a
        JOIN Patients p     ON a.patient_id  = p.patient_id
        JOIN Doctors d      ON a.doctor_id   = d.doctor_id
        JOIN Hospitals h    ON a.hospital_id = h.hospital_id
        WHERE a.patient_id = :patient_id
        ORDER BY a.appointment_date DESC
    """)
    return db.execute(sql, {"patient_id": patient_id}).mappings().all()



# 7. AGGREGATION — Count patients per disease

def get_patient_count_per_disease(db: Session):
    sql = text("""
        SELECT
            d.name          AS disease_name,
            d.category,
            COUNT(pd.patient_id) AS patient_count
        FROM Diseases d
        LEFT JOIN Patient_Diseases pd ON d.disease_id = pd.disease_id
        GROUP BY d.disease_id, d.name, d.category
        ORDER BY patient_count DESC
    """)
    return db.execute(sql).mappings().all()



# 8. AGGREGATION — Total order value across all orders

def get_total_order_value(db: Session):
    sql = text("""
        SELECT
            COUNT(order_id)         AS total_orders,
            SUM(total_amount)       AS total_revenue,
            AVG(total_amount)       AS avg_order_value,
            MAX(total_amount)       AS max_order,
            MIN(total_amount)       AS min_order
        FROM Orders
        WHERE status != 'Cancelled'
    """)
    return db.execute(sql).mappings().first()



# 9. AGGREGATION — Top selling medicines by quantity ordered

def get_top_selling_medications(db: Session, limit: int = 5):
    sql = text("""
        SELECT
            m.name              AS medication_name,
            m.category,
            SUM(oi.quantity)    AS total_qty_sold,
            SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM Order_Items oi
        JOIN Inventory inv   ON oi.inventory_id  = inv.inventory_id
        JOIN Medications m   ON inv.medication_id = m.medication_id
        GROUP BY m.medication_id, m.name, m.category
        ORDER BY total_qty_sold DESC
        LIMIT :limit
    """)
    return db.execute(sql, {"limit": limit}).mappings().all()



# 10. GROUPING — Cheapest available medicine per category

def get_cheapest_medicine_per_category(db: Session):
    sql = text("""
        SELECT
            m.category,
            m.name              AS medication_name,
            MIN(inv.price)      AS min_price,
            inv.stock
        FROM Inventory inv
        JOIN Medications m ON inv.medication_id = m.medication_id
        WHERE inv.stock > 0
        GROUP BY m.category, m.medication_id, m.name, inv.stock
        ORDER BY m.category, min_price
    """)
    return db.execute(sql).mappings().all()


# 11. GROUPING — Orders count and total spend per patient

def get_orders_per_patient(db: Session):
    sql = text("""
        SELECT
            p.name              AS patient_name,
            COUNT(o.order_id)   AS total_orders,
            SUM(o.total_amount) AS total_spent,
            MAX(o.order_date)   AS last_order_date
        FROM Patients p
        LEFT JOIN Orders o ON p.patient_id = o.patient_id
        GROUP BY p.patient_id, p.name
        ORDER BY total_spent DESC
    """)
    return db.execute(sql).mappings().all()


# 12. SUBQUERY — Patients with no disease recorded
def get_patients_without_disease(db: Session):
    sql = text("""
        SELECT
            patient_id,
            name,
            age,
            gender
        FROM Patients
        WHERE patient_id NOT IN (
            SELECT DISTINCT patient_id
            FROM Patient_Diseases
        )
        ORDER BY name
    """)
    return db.execute(sql).mappings().all()


# 13. ADDITIONAL — Total medicines in inventory with stock info

def get_inventory_summary(db: Session):
    sql = text("""
        SELECT
            COUNT(inv.inventory_id)     AS total_entries,
            SUM(inv.stock)              AS total_stock_units,
            COUNT(DISTINCT inv.medication_id) AS unique_medications,
            COUNT(DISTINCT inv.vendor_id)     AS active_vendors
        FROM Inventory inv
    """)
    return db.execute(sql).mappings().first()



# 14. ADDITIONAL — Vendors and medicines they supply
def get_vendor_supply_list(db: Session):
    sql = text("""
        SELECT
            v.name              AS vendor_name,
            v.contact_person,
            COUNT(inv.inventory_id)  AS medicines_supplied,
            SUM(inv.stock)           AS total_stock,
            MIN(inv.price)           AS lowest_price,
            MAX(inv.price)           AS highest_price
        FROM Vendors v
        JOIN Inventory inv ON v.vendor_id = inv.vendor_id
        GROUP BY v.vendor_id, v.name, v.contact_person
        ORDER BY medicines_supplied DESC
    """)
    return db.execute(sql).mappings().all()


# 15. ADDITIONAL — Symptoms reported by a patient
def get_patient_symptoms(db: Session, patient_id: str):
    sql = text("""
        SELECT
            p.name          AS patient_name,
            s.name          AS symptom,
            s.description,
            ps.reported_on
        FROM Patient_Symptoms ps
        JOIN Patients p  ON ps.patient_id = p.patient_id
        JOIN Symptoms s  ON ps.symptom_id = s.symptom_id
        WHERE ps.patient_id = :patient_id
        ORDER BY ps.reported_on DESC
    """)
    return db.execute(sql, {"patient_id": patient_id}).mappings().all()



# 16. ADDITIONAL — All diseases with their mapped medications
def get_disease_medication_map(db: Session):
    sql = text("""
        SELECT
            d.name          AS disease_name,
            d.category      AS disease_category,
            m.name          AS medication_name,
            m.category      AS medication_category,
            m.strength
        FROM Diseases d
        JOIN Disease_Medications dm ON d.disease_id    = dm.disease_id
        JOIN Medications m          ON dm.medication_id = m.medication_id
        ORDER BY d.name, m.name
    """)
    return db.execute(sql).mappings().all()



# 17. ADDITIONAL — Orders for a specific patient with items
def get_patient_orders(db: Session, patient_id: str):
    sql = text("""
        SELECT
            o.order_id,
            o.order_date,
            o.status,
            o.total_amount,
            m.name          AS medication_name,
            oi.quantity,
            oi.unit_price,
            (oi.quantity * oi.unit_price) AS line_total
        FROM Orders o
        JOIN Order_Items oi  ON o.order_id       = oi.order_id
        JOIN Inventory inv   ON oi.inventory_id  = inv.inventory_id
        JOIN Medications m   ON inv.medication_id = m.medication_id
        WHERE o.patient_id = :patient_id
        ORDER BY o.order_date DESC
    """)
    return db.execute(sql, {"patient_id": patient_id}).mappings().all()


# 18. ADDITIONAL — Medicine stock availability across vendors
def get_stock_availability(db: Session):
    sql = text("""
        SELECT
            inv.inventory_id,
            m.name              AS medication_name,
            m.category,
            m.strength,
            v.name              AS vendor_name,
            inv.price,
            inv.stock,
            inv.expiry_date,
            CASE
                WHEN inv.stock = 0      THEN 'Out of Stock'
                WHEN inv.stock < 50     THEN 'Low Stock'
                WHEN inv.stock < 200    THEN 'Moderate'
                ELSE                        'Well Stocked'
            END AS stock_status
        FROM Inventory inv
        JOIN Medications m  ON inv.medication_id = m.medication_id
        JOIN Vendors v      ON inv.vendor_id     = v.vendor_id
        ORDER BY inv.stock ASC
    """)
    return db.execute(sql).mappings().all()