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
        SELECT bill_id, bill_date, total
        FROM bills
        ORDER BY bill_id ASC
        """
    )

    return cursor.fetchall()
def save_bill_and_update_stock(total, bill_items):
    try:
        
        db.start_transaction()

        
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
