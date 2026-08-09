from db_connection import db, cursor


def get_medicine_stock(name):
    cursor.execute(
        """
        SELECT quantity, price
        FROM medicines
        WHERE LOWER(name) = LOWER(%s)
        """,
        (name,)
    )
    return cursor.fetchone()



def get_bill_history():
    cursor.execute(
        """
        SELECT
            b.bill_id,
            b.bill_date,
            GROUP_CONCAT(bi.medicine_name SEPARATOR ', '),
            GROUP_CONCAT(bi.quantity SEPARATOR ', '),
            b.total
        FROM bills b
        LEFT JOIN bill_items bi
            ON b.bill_id = bi.bill_id
        GROUP BY b.bill_id, b.bill_date, b.total
        ORDER BY b.bill_id ASC
        """
    )

    return cursor.fetchall()

    return cursor.fetchall()
def save_bill_and_update_stock(total, bill_items):
    try:
        
    

        
        cursor.execute(
            "INSERT INTO bills (total) VALUES (%s)",
            (total,)
        )

        bill_id = cursor.lastrowid

        
        for item in bill_items:
            name, qty, price, subtotal = item

            
            cursor.execute(
                """
                UPDATE medicines
                SET quantity = quantity - %s
                WHERE LOWER(name) = LOWER(%s)
                AND quantity >= %s
                """,
                (qty, name, qty)
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Insufficient stock for {name}"
                )
            cursor.execute(
                """
                INSERT INTO bill_items
                (bill_id, medicine_name, quantity, price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (bill_id, name, qty, price, subtotal)
            )

        db.commit()

        return bill_id

    except Exception:
        db.rollback()
        
        raise
