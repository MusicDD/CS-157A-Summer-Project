from User.db import get_connection

# CREATE / READ
def create_admin(first_name, last_name, email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Admin (firstName, lastName, email) VALUES (%s, %s, %s)",
        (first_name, last_name, email),
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def get_all_admins():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Admin")
    admins = cursor.fetchall()
    cursor.close()
    connection.close()
    return admins


def get_admin_by_id(admin_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Admin WHERE adminId = %s", (admin_id,))
    admin = cursor.fetchone()
    cursor.close()
    connection.close()
    return admin


def get_admin_by_email(email):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Admin WHERE email = %s", (email,))
    admin = cursor.fetchone()
    cursor.close()
    connection.close()
    return admin


# Banning users (Admin -> User relationship)
def ban_user(user_id, admin_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE User SET bannedByAdminId = %s WHERE userId = %s", (admin_id, user_id)
    )
    connection.commit()
    cursor.close()
    connection.close()


def unban_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE User SET bannedByAdminId = NULL WHERE userId = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()


def get_users_banned_by(admin_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT userId, firstName, lastName, username FROM User WHERE bannedByAdminId = %s",
        (admin_id,),
    )
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users


# AdminManagesClub (many-to-many)
def assign_admin_to_club(admin_id, club_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT IGNORE INTO AdminManagesClub (adminId, clubId) VALUES (%s, %s)",
        (admin_id, club_id),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_clubs_managed_by_admin(admin_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Clubs.* FROM Clubs
        JOIN AdminManagesClub ON Clubs.clubId = AdminManagesClub.clubId
        WHERE AdminManagesClub.adminId = %s
        """,
        (admin_id,),
    )
    clubs = cursor.fetchall()
    cursor.close()
    connection.close()
    return clubs