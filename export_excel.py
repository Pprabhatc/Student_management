import pandas as pd
from db import connect_db

def export_students():

    conn = connect_db()

    query = "SELECT * FROM students"

    df = pd.read_sql(query, conn)

    df.to_excel(
        "reports/student_report.xlsx",
        index=False
    )

    conn.close()

    return True