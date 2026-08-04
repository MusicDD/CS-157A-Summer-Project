from User.db import get_connection

# Broadcast (ISA parent)
def _create_broadcast(cursor, club_id):
    """Internal helper: inserts the shared Broadcast row, returns its id."""
    cursor.execute(
        "INSERT INTO Broadcast (broadcastTimestamp, clubId) VALUES (NOW(), %s)",
        (club_id,),
    )
    return cursor.lastrowid


def get_broadcast_by_id(broadcast_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Broadcast WHERE broadcastId = %s", (broadcast_id,))
    broadcast = cursor.fetchone()
    cursor.close()
    connection.close()
    return broadcast


def get_broadcasts_for_club(club_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Broadcast WHERE clubId = %s ORDER BY broadcastTimestamp DESC",
        (club_id,),
    )
    broadcasts = cursor.fetchall()
    cursor.close()
    connection.close()
    return broadcasts


def add_broadcast_author(broadcast_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT IGNORE INTO BroadcastAuthors (broadcastId, userId) VALUES (%s, %s)",
        (broadcast_id, user_id),
    )
    connection.commit()
    cursor.close()
    connection.close()

# EventUpdate (Broadcast subtype)
def create_event_update(club_id, author_user_id, event_date, event_location, event_description):
    connection = get_connection()
    cursor = connection.cursor()

    broadcast_id = _create_broadcast(cursor, club_id)
    cursor.execute(
        """
        INSERT INTO EventUpdate (broadcastId, eventDate, eventLocation, eventDescription)
        VALUES (%s, %s, %s, %s)
        """,
        (broadcast_id, event_date, event_location, event_description),
    )
    cursor.execute(
        "INSERT INTO BroadcastAuthors (broadcastId, userId) VALUES (%s, %s)",
        (broadcast_id, author_user_id),
    )

    connection.commit()
    cursor.close()
    connection.close()
    return broadcast_id


def get_event_updates_for_club(club_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Broadcast.broadcastId, Broadcast.broadcastTimestamp,
               EventUpdate.eventDate, EventUpdate.eventLocation, EventUpdate.eventDescription
        FROM Broadcast
        JOIN EventUpdate ON Broadcast.broadcastId = EventUpdate.broadcastId
        WHERE Broadcast.clubId = %s
        ORDER BY Broadcast.broadcastTimestamp DESC
        """,
        (club_id,),
    )
    events = cursor.fetchall()
    cursor.close()
    connection.close()
    return events

# Poll (Broadcast subtype)
def create_poll(club_id, author_user_id, poll_question, poll_close_date=None):
    connection = get_connection()
    cursor = connection.cursor()

    broadcast_id = _create_broadcast(cursor, club_id)
    cursor.execute(
        "INSERT INTO Poll (broadcastId, pollQuestion, pollCloseDate) VALUES (%s, %s, %s)",
        (broadcast_id, poll_question, poll_close_date),
    )
    cursor.execute(
        "INSERT INTO BroadcastAuthors (broadcastId, userId) VALUES (%s, %s)",
        (broadcast_id, author_user_id),
    )

    connection.commit()
    cursor.close()
    connection.close()
    return broadcast_id


def get_polls_for_club(club_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Broadcast.broadcastId, Broadcast.broadcastTimestamp,
               Poll.pollQuestion, Poll.pollCloseDate
        FROM Broadcast
        JOIN Poll ON Broadcast.broadcastId = Poll.broadcastId
        WHERE Broadcast.clubId = %s
        ORDER BY Broadcast.broadcastTimestamp DESC
        """,
        (club_id,),
    )
    polls = cursor.fetchall()
    cursor.close()
    connection.close()
    return polls

# Announcement (Broadcast subtype)
def create_announcement(club_id, author_user_id, announcement_text):
    connection = get_connection()
    cursor = connection.cursor()

    broadcast_id = _create_broadcast(cursor, club_id)
    cursor.execute(
        "INSERT INTO Announcement (broadcastId, announcementText) VALUES (%s, %s)",
        (broadcast_id, announcement_text),
    )
    cursor.execute(
        "INSERT INTO BroadcastAuthors (broadcastId, userId) VALUES (%s, %s)",
        (broadcast_id, author_user_id),
    )

    connection.commit()
    cursor.close()
    connection.close()
    return broadcast_id

def get_announcements_for_club(club_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT Broadcast.broadcastId, Broadcast.broadcastTimestamp, Announcement.announcementText
        FROM Broadcast
        JOIN Announcement ON Broadcast.broadcastId = Announcement.broadcastId
        WHERE Broadcast.clubId = %s
        ORDER BY Broadcast.broadcastTimestamp DESC
        """,
        (club_id,),
    )
    announcements = cursor.fetchall()
    cursor.close()
    connection.close()
    return announcements

def get_feed_for_club(club_id):
    """
    Combines EventUpdates, Polls, and Announcements for a club into one
    feed, newest first -- this is what powers the dashboard's post list.
    """
    events = get_event_updates_for_club(club_id)
    for e in events:
        e["type"] = "event"

    polls = get_polls_for_club(club_id)
    for p in polls:
        p["type"] = "poll"

    announcements = get_announcements_for_club(club_id)
    for a in announcements:
        a["type"] = "announcement"

    feed = events + polls + announcements
    feed.sort(key=lambda item: item["broadcastTimestamp"], reverse=True)
    return feed

# Notification (fans a broadcast out to individual users)
def notify_user(user_id, broadcast_id, content):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO Notification (content, isRead, sentTimestamp, broadcastId, userId)
        VALUES (%s, FALSE, NOW(), %s, %s)
        """,
        (content, broadcast_id, user_id),
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def notify_club_members(club_id, broadcast_id, content):
    """Sends the same notification to every member of a club."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT userId FROM Membership WHERE clubId = %s", (club_id,))
    member_ids = [row["userId"] for row in cursor.fetchall()]
    cursor.close()
    connection.close()

    for user_id in member_ids:
        notify_user(user_id, broadcast_id, content)

    return len(member_ids)


def get_notifications_for_user(user_id, unread_only=False):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    if unread_only:
        cursor.execute(
            "SELECT * FROM Notification WHERE userId = %s AND isRead = FALSE ORDER BY sentTimestamp DESC",
            (user_id,),
        )
    else:
        cursor.execute(
            "SELECT * FROM Notification WHERE userId = %s ORDER BY sentTimestamp DESC",
            (user_id,),
        )
    notifications = cursor.fetchall()
    cursor.close()
    connection.close()
    return notifications


def mark_notification_read(notification_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Notification SET isRead = TRUE WHERE notificationId = %s", (notification_id,)
    )
    connection.commit()
    cursor.close()
    connection.close()