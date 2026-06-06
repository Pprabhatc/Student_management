from db import connect_db

def check_login(username, password):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM admin
        WHERE username=%s
        AND password=%s
        """,
        (username, password)
    )

    result = cursor.fetchone()

    conn.close()

    return result