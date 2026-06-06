from tkinter import *
from tkinter import ttk, messagebox
from db import connect_db
from login import check_login

root = Tk()
root.title("Student Management System")
root.geometry("1000x650")
root.withdraw()

# ---------------- LOGIN WINDOW ---------------- #

login_window = Toplevel(root)
login_window.title("Admin Login")
login_window.geometry("350x250")
login_window.resizable(False, False)

# ---------------- VARIABLES ---------------- #

username_var = StringVar()
password_var = StringVar()

name_var = StringVar()
age_var = StringVar()
gender_var = StringVar()
course_var = StringVar()
phone_var = StringVar()
email_var = StringVar()
search_var = StringVar()

# ---------------- LOGIN FUNCTION ---------------- #

def login():

    username = username_var.get()
    password = password_var.get()

    result = check_login(
        username,
        password
    )

    if result:

        login_window.destroy()
        root.deiconify()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )

# ---------------- VALIDATION ---------------- #

def validate():

    if name_var.get() == "":
        messagebox.showwarning(
            "Validation",
            "Enter Student Name"
        )
        return False

    if age_var.get() == "":
        messagebox.showwarning(
            "Validation",
            "Enter Age"
        )
        return False

    return True

# ---------------- CLEAR FIELDS ---------------- #

def clear_fields():

    name_var.set("")
    age_var.set("")
    gender_var.set("")
    course_var.set("")
    phone_var.set("")
    email_var.set("")

# ---------------- ADD STUDENT ---------------- #

def add_student():

    if not validate():
        return

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    INSERT INTO students
    (name, age, gender, course, phone, email)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    values = (
        name_var.get(),
        age_var.get(),
        gender_var.get(),
        course_var.get(),
        phone_var.get(),
        email_var.get()
    )

    cursor.execute(sql, values)

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Student Added Successfully"
    )

    clear_fields()
    show_students()


# ---------------- SHOW STUDENTS ---------------- #

def show_students():

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()


# ---------------- SEARCH STUDENT ---------------- #

def search_student():

    sid = search_var.get()

    if sid == "":
        show_students()
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (sid,)
    )

    row = cursor.fetchone()

    for item in tree.get_children():
        tree.delete(item)

    if row:
        tree.insert("", END, values=row)
    else:
        messagebox.showinfo(
            "Not Found",
            "Student Not Found"
        )

    conn.close()


# ---------------- DELETE STUDENT ---------------- #

def delete_student():

    selected = tree.focus()

    if selected == "":
        messagebox.showwarning(
            "Warning",
            "Select a Student"
        )
        return

    data = tree.item(selected)

    sid = data["values"][0]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id=%s",
        (sid,)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Deleted",
        "Student Deleted Successfully"
    )

    show_students()


# ---------------- UPDATE STUDENT ---------------- #

def update_student():

    selected = tree.focus()

    if selected == "":
        messagebox.showwarning(
            "Warning",
            "Select a Student"
        )
        return

    data = tree.item(selected)

    sid = data["values"][0]

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    UPDATE students
    SET
    name=%s,
    age=%s,
    gender=%s,
    course=%s,
    phone=%s,
    email=%s
    WHERE student_id=%s
    """

    cursor.execute(
        sql,
        (
            name_var.get(),
            age_var.get(),
            gender_var.get(),
            course_var.get(),
            phone_var.get(),
            email_var.get(),
            sid
        )
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Updated",
        "Student Updated Successfully"
    )

    show_students()


# ---------------- TREE CLICK ---------------- #

def get_cursor(event):

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    if values:

        name_var.set(values[1])
        age_var.set(values[2])
        gender_var.set(values[3])
        course_var.set(values[4])
        phone_var.set(values[5])
        email_var.set(values[6])

# ---------------- TITLE ---------------- #

Label(
    root,
    text="Student Management System",
    font=("Arial", 20, "bold")
).pack(pady=10)

# ---------------- LEFT FRAME ---------------- #

left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=20)

Label(left_frame, text="Name").grid(row=0, column=0, pady=5)
Entry(left_frame, textvariable=name_var).grid(row=0, column=1)

Label(left_frame, text="Age").grid(row=1, column=0, pady=5)
Entry(left_frame, textvariable=age_var).grid(row=1, column=1)

Label(left_frame, text="Gender").grid(row=2, column=0, pady=5)

gender_combo = ttk.Combobox(
    left_frame,
    textvariable=gender_var,
    values=["Male", "Female", "Other"],
    state="readonly"
)

gender_combo.grid(row=2, column=1)

Label(left_frame, text="Course").grid(row=3, column=0, pady=5)
Entry(left_frame, textvariable=course_var).grid(row=3, column=1)

Label(left_frame, text="Phone").grid(row=4, column=0, pady=5)
Entry(left_frame, textvariable=phone_var).grid(row=4, column=1)

Label(left_frame, text="Email").grid(row=5, column=0, pady=5)
Entry(left_frame, textvariable=email_var).grid(row=5, column=1)

# ---------------- BUTTONS ---------------- #

Button(
    left_frame,
    text="Add Student",
    width=15,
    command=add_student
).grid(row=6, column=0, pady=10)

Button(
    left_frame,
    text="Update Student",
    width=15,
    command=update_student
).grid(row=6, column=1)

Button(
    left_frame,
    text="Delete Student",
    width=15,
    command=delete_student
).grid(row=7, column=0)

Button(
    left_frame,
    text="Clear",
    width=15,
    command=clear_fields
).grid(row=7, column=1)

# ---------------- SEARCH ---------------- #

Label(
    left_frame,
    text="Student ID"
).grid(row=8, column=0, pady=10)

Entry(
    left_frame,
    textvariable=search_var
).grid(row=8, column=1)

Button(
    left_frame,
    text="Search",
    width=15,
    command=search_student
).grid(row=9, column=0)

Button(
    left_frame,
    text="Show All",
    width=15,
    command=show_students
).grid(row=9, column=1)

# ---------------- TABLE ---------------- #

tree = ttk.Treeview(
    root,
    columns=(
        "ID",
        "Name",
        "Age",
        "Gender",
        "Course",
        "Phone",
        "Email"
    ),
    show="headings"
)

for col in (
    "ID",
    "Name",
    "Age",
    "Gender",
    "Course",
    "Phone",
    "Email"
):

    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(
    side=RIGHT,
    fill=BOTH,
    expand=True,
    padx=10,
    pady=10
)

tree.bind(
    "<ButtonRelease-1>",
    get_cursor
)

show_students()

# ---------------- LOGIN WINDOW ---------------- #

Label(
    login_window,
    text="Admin Login",
    font=("Arial", 16, "bold")
).pack(pady=15)

Label(
    login_window,
    text="Username"
).pack()

Entry(
    login_window,
    textvariable=username_var
).pack()

Label(
    login_window,
    text="Password"
).pack()

Entry(
    login_window,
    textvariable=password_var,
    show="*"
).pack()

Button(
    login_window,
    text="Login",
    width=15,
    command=login
).pack(pady=15)

root.mainloop()