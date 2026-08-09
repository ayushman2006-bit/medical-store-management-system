from db_connection import db, cursor


def medicine_exists(name):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM medicines
        WHERE LOWER(name) = LOWER(%s)
        """,
        (name,)
    )
    return cursor.fetchone()[0] > 0


def add_medicine(name, quantity, price, expiry):
    cursor.execute(
        """
        INSERT INTO medicines(name, quantity, price, expiry)
        VALUES (%s, %s, %s, %s)
        """,
        (name, quantity, price, expiry)
    )
    db.commit()


def get_all_medicines():
    cursor.execute(
        """
        SELECT name, quantity, price, expiry
        FROM medicines
        """
    )
    return cursor.fetchall()


def get_medicine(name):
    cursor.execute(
        """
        SELECT name, quantity, price, expiry
        FROM medicines
        WHERE LOWER(name) = LOWER(%s)
        """,
        (name,)
    )
    return cursor.fetchone()


def update_medicine(name, quantity, price, expiry):
    cursor.execute(
        """
        UPDATE medicines
        SET quantity=%s,
            price=%s,
            expiry=%s
        WHERE LOWER(name)=LOWER(%s)
        """,
        (quantity, price, expiry, name)
    )
    db.commit()

    return cursor.rowcount


def delete_medicine(name):
    cursor.execute(
        """
        DELETE FROM medicines
        WHERE LOWER(name)=LOWER(%s)
        """,
        (name,)
    )
    db.commit()

    return cursor.rowcount
def search_medicine_names(prefix):
    cursor.execute(
        """
        SELECT name
        FROM medicines
        WHERE LOWER(name) LIKE LOWER(%s)
        ORDER BY name
        """,
        (prefix + "%",)
    )

    return [row[0] for row in cursor.fetchall()]
def get_dashboard_stats():
    cursor.execute("SELECT COUNT(*) FROM medicines")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM medicines WHERE quantity < 10"
    )
    low_stock = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(quantity * price) FROM medicines"
    )
    value = cursor.fetchone()[0]

    if value is None:
        value = 0

    return total, low_stock, value
def get_expiring_medicines(warning_date):
    cursor.execute(
        """
        SELECT name, expiry
        FROM medicines
        WHERE expiry <= %s
        """,
        (warning_date,)
    )

    return cursor.fetchall()
