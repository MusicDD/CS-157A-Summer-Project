from User.db import get_connection

# PostThread
def create_post(author_user_id, content):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO PostThread (content, createdDate, authorUserId) VALUES (%s, CURDATE(), %s)",
        (content, author_user_id),
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def get_post_by_id(post_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM PostThread WHERE postId = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    connection.close()
    return post


def get_all_posts():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM PostThread ORDER BY createdDate DESC")
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return posts


def get_posts_by_author(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM PostThread WHERE authorUserId = %s ORDER BY createdDate DESC",
        (user_id,),
    )
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return posts

# Interaction
VALID_TYPES = {"like", "comment", "share", "tag"}
POST_TARGETED_TYPES = {"like", "comment", "tag"}
USER_TARGETED_TYPES = {"share"}

def create_interaction(interaction_type, initiator_user_id, content=None,
                        target_post_id=None, recipient_user_id=None):
    if interaction_type not in VALID_TYPES:
        raise ValueError(f"interaction_type must be one of {VALID_TYPES}")

    if interaction_type in POST_TARGETED_TYPES:
        if target_post_id is None or recipient_user_id is not None:
            raise ValueError(f"'{interaction_type}' requires target_post_id and no recipient_user_id")
    else:  # USER_TARGETED_TYPES
        if recipient_user_id is None or target_post_id is not None:
            raise ValueError(f"'{interaction_type}' requires recipient_user_id and no target_post_id")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO Interaction
            (interactionType, content, timestamp, initiatorUserId, targetPostId, recipientUserId)
        VALUES (%s, %s, NOW(), %s, %s, %s)
        """,
        (interaction_type, content, initiator_user_id, target_post_id, recipient_user_id),
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def get_interactions_for_post(post_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Interaction WHERE targetPostId = %s ORDER BY timestamp",
        (post_id,),
    )
    interactions = cursor.fetchall()
    cursor.close()
    connection.close()
    return interactions


def get_interactions_by_user(user_id):
    """Interactions this user initiated (their likes/comments/shares/tags)."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Interaction WHERE initiatorUserId = %s ORDER BY timestamp DESC",
        (user_id,),
    )
    interactions = cursor.fetchall()
    cursor.close()
    connection.close()
    return interactions


def get_shares_received_by_user(user_id):
    """Posts that have been shared with this user."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Interaction WHERE recipientUserId = %s AND interactionType = 'share' ORDER BY timestamp DESC",
        (user_id,),
    )
    interactions = cursor.fetchall()
    cursor.close()
    connection.close()
    return interactions