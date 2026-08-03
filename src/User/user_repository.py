import hashlib
from datetime import date
from .db import get_connection

def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
 
# Derived value: age, computed from dob
def get_user_age(dob):
    """
    Given a date of birth, returns the person's current age in years.
    Accepts either a datetime.date object or None.
    """
    if dob is None:
        return None
 
    today = date.today()
    years = today.year - dob.year
 
    # subtract 1 if their birthday hasn't happened yet this year
    had_birthday_this_year = (today.month, today.day) >= (dob.month, dob.day)
    if not had_birthday_this_year:
        years -= 1
 
    return years
 
 
# matches signup.html (name, username, password)
def create_user(first_name, last_name, username, email, password,
                 phone_number=None, dob=None):
    connection = get_connection()
    cursor = connection.cursor()
 
    sql = """
        INSERT INTO users
            (first_name, last_name, username, email, phone_number, dob, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        first_name, last_name, username, email,
        phone_number, dob, hash_password(password),
    )
 
    cursor.execute(sql, values)
    connection.commit()
    new_id = cursor.lastrowid
 
    cursor.close()
    connection.close()
    return new_id
 
# READ
def get_user_by_id(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
 
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
 
    cursor.close()
    connection.close()
 
    if user is not None:
        user["age"] = get_user_age(user.get("dob"))  # computed, not stored
 
    return user
 
 
def get_user_by_username(username):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
 
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
 
    cursor.close()
    connection.close()
 
    if user is not None:
        user["age"] = get_user_age(user.get("dob"))
 
    return user
 
 
def get_all_users():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
 
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
 
    cursor.close()
    connection.close()
 
    for user in users:
        user["age"] = get_user_age(user.get("dob"))
 
    return users
 

# matches login.html (username, password)
def authenticate_user(username, password):
    user = get_user_by_username(username)
 
    if user is None:
        return None
 
    if user["password_hash"] == hash_password(password):
        return user
 
    return None
 
 

# matches settings.html (name, etc.)
def update_user(user_id, **fields):
    if not fields:
        return
 
    # age is never a real column, so silently ignore it if it's passed in
    fields.pop("age", None)
    if not fields:
        return
 
    columns = ", ".join(f"{key} = %s" for key in fields)
    values = list(fields.values()) + [user_id]
 
    connection = get_connection()
    cursor = connection.cursor()
 
    cursor.execute(f"UPDATE users SET {columns} WHERE user_id = %s", values)
    connection.commit()
 
    cursor.close()
    connection.close()
 
 
# -----------------------------------------------------------------
# DELETE
# -----------------------------------------------------------------
def delete_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()
 
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    connection.commit()
 
    cursor.close()
    connection.close()
 
 
# -----------------------------------------------------------------
# ADMIN (ISA subtype of User)
# -----------------------------------------------------------------
def make_admin(user_id):
    """Promotes an existing user to admin by adding a row to `admins`."""
    connection = get_connection()
    cursor = connection.cursor()
 
    cursor.execute("INSERT IGNORE INTO admins (user_id) VALUES (%s)", (user_id,))
    connection.commit()
 
    cursor.close()
    connection.close()
 
 
def is_admin(user_id):
    connection = get_connection()
    cursor = connection.cursor()
 
    cursor.execute("SELECT 1 FROM admins WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
 
    cursor.close()
    connection.close()
    return result is not None
