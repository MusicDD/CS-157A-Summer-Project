import hashlib
from datetime import date
from .db import get_connection


def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()


def get_user_age(dob):
    if dob is None:
        return None
    today = date.today()
    years = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        years -= 1
    return years

# CREATE
def create_user(first_name, last_name, username, dob, password, emails=None, phones=None):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        (first_name, last_name, username, dob, hash_password(password)),
    )
    user_id = cursor.lastrowid

    for email in (emails or []):
        cursor.execute(
            "INSERT INTO UserEmail (userId, email) VALUES (%s, %s)", (user_id, email)
        )

    for phone in (phones or []):
        cursor.execute(
            "INSERT INTO UserPhone (userId, phone) VALUES (%s, %s)", (user_id, phone)
        )

    connection.commit()
    cursor.close()
    connection.close()
    return user_id


def add_email(user_id, email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO UserEmail (userId, email) VALUES (%s, %s)", (user_id, email))
    connection.commit()
    cursor.close()
    connection.close()


def add_phone(user_id, phone):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO UserPhone (userId, phone) VALUES (%s, %s)", (user_id, phone))
    connection.commit()
    cursor.close()
    connection.close()

# READ
def get_user_emails(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT email FROM UserEmail WHERE userId = %s", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return [row["email"] for row in rows]


def get_user_phones(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT phone FROM UserPhone WHERE userId = %s", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return [row["phone"] for row in rows]


def _attach_extras(user):
    if user is None:
        return None
    user["age"] = get_user_age(user.get("DoB"))
    user["emails"] = get_user_emails(user["userId"])
    user["phones"] = get_user_phones(user["userId"])
    return user


def get_user_by_id(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User WHERE userId = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return _attach_extras(user)


def get_user_by_username(username):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return _attach_extras(user)


def get_all_users():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return [_attach_extras(u) for u in users]

# LOGIN
def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user is None:
        return None
    if user["passwordHash"] == hash_password(password):
        return user
    return None

# UPDATE / DELETE
def update_user(user_id, **fields):
    fields.pop("age", None)
    fields.pop("emails", None)
    fields.pop("phones", None)
    if not fields:
        return

    columns = ", ".join(f"{key} = %s" for key in fields)
    values = list(fields.values()) + [user_id]

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE User SET {columns} WHERE userId = %s", values)
    connection.commit()
    cursor.close()
    connection.close()


def delete_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM User WHERE userId = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()