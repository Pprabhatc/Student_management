from db import connect_db
from datetime import date

def mark_attendance(student_id,status):

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    INSERT INTO attendance
    (student_id,attendance_date,status)
    VALUES(%s,%s,%s)
    """

    cursor.execute(
        sql,
        (
            student_id,
            date.today(),
            status
        )
    )

    conn.commit()
    conn.close()