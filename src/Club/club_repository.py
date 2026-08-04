from User.db import get_connection

# CLUBS
def create_club(club_name, club_focus=None, club_status="active"):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO Clubs (clubName, clubStatus, clubFocus, lastActivityDate)
        VALUES (%s, %s, %s, CURDATE())
        """,
        (club_name, club_status, club_focus),
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def get_all_clubs(status=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    if status:
        cursor.execute("SELECT * FROM Clubs WHERE clubStatus = %s", (status,))
    else:
        cursor.execute("SELECT * FROM Clubs")
    clubs = cursor.fetchall()
    cursor.close()
    connection.close()
    return clubs


def get_club_by_id(club_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Clubs WHERE clubId = %s", (club_id,))
    club = cursor.fetchone()
    cursor.close()
    connection.close()
    return club


def get_club_by_name(club_name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Clubs WHERE clubName = %s", (club_name,))
    club = cursor.fetchone()
    cursor.close()
    connection.close()
    return club


def update_club(club_id, **fields):
    if not fields:
        return
    columns = ", ".join(f"{key} = %s" for key in fields)
    values = list(fields.values()) + [club_id]
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Clubs SET {columns} WHERE clubId = %s", values)
    connection.commit()
    cursor.close()
    connection.close()


# Club_Manager (ISA subtype of User)
def make_club_manager(user_id, start_date=None):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT IGNORE INTO Club_Manager (userId, startDate) VALUES (%s, COALESCE(%s, CURDATE()))",
        (user_id, start_date),
    )
    connection.commit()
    cursor.close()
    connection.close()


def is_club_manager(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Club_Manager WHERE userId = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None


def set_manager_role(user_id, role):
    """
    role is one of "social_media", "event_coordinator", "chat_moderator".
    The user must already be a Club_Manager (call make_club_manager first).
    """
    table_by_role = {
        "social_media": "SocialMediaManager",
        "event_coordinator": "EventCoordinator",
        "chat_moderator": "ChatModerator",
    }
    table = table_by_role.get(role)
    if table is None:
        raise ValueError(f"Unknown role: {role}")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT IGNORE INTO {table} (userId) VALUES (%s)", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()


def get_manager_roles(user_id):
    """Returns which of the three specialist roles this manager holds."""
    connection = get_connection()
    cursor = connection.cursor()
    roles = []
    for role, table in [
        ("social_media", "SocialMediaManager"),
        ("event_coordinator", "EventCoordinator"),
        ("chat_moderator", "ChatModerator"),
    ]:
        cursor.execute(f"SELECT 1 FROM {table} WHERE userId = %s", (user_id,))
        if cursor.fetchone():
            roles.append(role)
    cursor.close()
    connection.close()
    return roles

# ClubManagement (many-to-many)
def assign_manager_to_club(club_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT IGNORE INTO ClubManagement (clubId, userId) VALUES (%s, %s)",
        (club_id, user_id),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_managers_of_club(club_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT User.userId, User.firstName, User.lastName, User.username
        FROM User
        JOIN ClubManagement ON User.userId = ClubManagement.userId
        WHERE ClubManagement.clubId = %s
        """,
        (club_id,),
    )
    managers = cursor.fetchall()
    cursor.close()
    connection.close()
    return managers


def get_clubs_managed_by(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Clubs.* FROM Clubs
        JOIN ClubManagement ON Clubs.clubId = ClubManagement.clubId
        WHERE ClubManagement.userId = %s
        """,
        (user_id,),
    )
    clubs = cursor.fetchall()
    cursor.close()
    connection.close()
    return clubs

# Membership (the Join relationship: User <-> Club)
def join_club(user_id, club_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT IGNORE INTO Membership (userId, clubId, dateJoined) VALUES (%s, %s, CURDATE())",
        (user_id, club_id),
    )
    connection.commit()
    joined_new_row = cursor.rowcount > 0
    cursor.close()
    connection.close()
    return joined_new_row


def leave_club(user_id, club_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM Membership WHERE userId = %s AND clubId = %s", (user_id, club_id)
    )
    connection.commit()
    cursor.close()
    connection.close()


def is_member(user_id, club_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT 1 FROM Membership WHERE userId = %s AND clubId = %s", (user_id, club_id)
    )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None


def get_clubs_for_user(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Clubs.*, Membership.dateJoined
        FROM Clubs
        JOIN Membership ON Clubs.clubId = Membership.clubId
        WHERE Membership.userId = %s
        """,
        (user_id,),
    )
    clubs = cursor.fetchall()
    cursor.close()
    connection.close()
    return clubs


def get_members_of_club(club_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT User.userId, User.firstName, User.lastName, User.username, Membership.dateJoined
        FROM User
        JOIN Membership ON User.userId = Membership.userId
        WHERE Membership.clubId = %s
        """,
        (club_id,),
    )
    members = cursor.fetchall()
    cursor.close()
    connection.close()
    return members

# ClubFormationRequest (a User proposes a new Club)
def submit_club_request(user_id, proposed_name, intention=None, activities=None):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO ClubFormationRequest
            (userId, proposedClubName, club_Intention, proposedClubActivities, status, requestDate)
        VALUES (%s, %s, %s, %s, 'pending', CURDATE())
        """,
        (user_id, proposed_name, intention, activities),
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def review_club_request(request_id, admin_id, approve):
    """approve=True -> status 'approved', approve=False -> 'denied'."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE ClubFormationRequest
        SET status = %s, reviewedByAdminId = %s
        WHERE requestId = %s
        """,
        ("approved" if approve else "denied", admin_id, request_id),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_club_requests(status=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    if status:
        cursor.execute("SELECT * FROM ClubFormationRequest WHERE status = %s", (status,))
    else:
        cursor.execute("SELECT * FROM ClubFormationRequest")
    requests = cursor.fetchall()
    cursor.close()
    connection.close()
    return requests