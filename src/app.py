"""
Run with (from inside src/):
    python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from User import user_repository as users
from Admin import admin_repository as admins
from Club import club_repository as clubs
from Broadcast import broadcast_repository as broadcasts
from Social import social_repository as social

app = Flask(__name__)
CORS(app)


def bad_request(message):
    return jsonify({"error": message}), 400


def not_found(message):
    return jsonify({"error": message}), 404

# USERS
@app.route("/api/signup", methods=["POST"])
def signup():
    """
    { "firstName", "username", "dob" (YYYY-MM-DD), "password",
      "lastName" (optional), "emails": [...] (optional), "phones": [...] (optional) }
    """
    data = request.get_json()
    required = ["firstName", "username", "dob", "password"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return bad_request(f"Missing fields: {', '.join(missing)}")

    if users.get_user_by_username(data["username"]):
        return jsonify({"error": "Username already taken"}), 409

    user_id = users.create_user(
        first_name=data["firstName"],
        last_name=data.get("lastName", ""),
        username=data["username"],
        dob=data["dob"],
        password=data["password"],
        emails=data.get("emails"),
        phones=data.get("phones"),
    )
    return jsonify({"message": "Account created", "userId": user_id}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")
    if not username or not password:
        return bad_request("Username and password are required")

    user = users.authenticate_user(username, password)
    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    if user.get("bannedByAdminId") is not None:
        return jsonify({"error": "This account has been banned"}), 403

    user.pop("passwordHash", None)
    return jsonify({"message": "Login successful", "user": user}), 200


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get_user_by_id(user_id)
    if user is None:
        return not_found("User not found")
    user.pop("passwordHash", None)
    return jsonify(user), 200


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    users.update_user(user_id, **request.get_json())
    return jsonify({"message": "User updated"}), 200


@app.route("/api/users/<int:user_id>/emails", methods=["POST"])
def add_email_route(user_id):
    email = request.get_json().get("email")
    if not email:
        return bad_request("email is required")
    users.add_email(user_id, email)
    return jsonify({"message": "Email added"}), 201


@app.route("/api/users/<int:user_id>/phones", methods=["POST"])
def add_phone_route(user_id):
    phone = request.get_json().get("phone")
    if not phone:
        return bad_request("phone is required")
    users.add_phone(user_id, phone)
    return jsonify({"message": "Phone added"}), 201

# ADMIN
@app.route("/api/admins", methods=["GET"])
def list_admins():
    return jsonify(admins.get_all_admins()), 200


@app.route("/api/admins", methods=["POST"])
def create_admin_route():
    data = request.get_json()
    required = ["firstName", "lastName", "email"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return bad_request(f"Missing fields: {', '.join(missing)}")
    new_id = admins.create_admin(data["firstName"], data["lastName"], data["email"])
    return jsonify({"message": "Admin created", "adminId": new_id}), 201


@app.route("/api/users/<int:user_id>/ban", methods=["POST"])
def ban_user_route(user_id):
    admin_id = request.get_json().get("adminId")
    if not admin_id:
        return bad_request("adminId is required")
    admins.ban_user(user_id, admin_id)
    return jsonify({"message": "User banned"}), 200


@app.route("/api/users/<int:user_id>/unban", methods=["POST"])
def unban_user_route(user_id):
    admins.unban_user(user_id)
    return jsonify({"message": "User unbanned"}), 200

# CLUBS
@app.route("/api/clubs", methods=["GET"])
def list_clubs():
    return jsonify(clubs.get_all_clubs(status=request.args.get("status"))), 200


@app.route("/api/clubs", methods=["POST"])
def create_club_route():
    data = request.get_json()
    club_name = data.get("clubName")
    if not club_name:
        return bad_request("clubName is required")
    if clubs.get_club_by_name(club_name):
        return jsonify({"error": "A club with that name already exists"}), 409
    new_id = clubs.create_club(club_name, data.get("clubFocus"), data.get("clubStatus", "active"))
    return jsonify({"message": "Club created", "clubId": new_id}), 201


@app.route("/api/clubs/<int:club_id>", methods=["GET"])
def get_club_route(club_id):
    club = clubs.get_club_by_id(club_id)
    if club is None:
        return not_found("Club not found")
    return jsonify(club), 200


@app.route("/api/clubs/<int:club_id>/members", methods=["GET"])
def get_club_members_route(club_id):
    if clubs.get_club_by_id(club_id) is None:
        return not_found("Club not found")
    return jsonify(clubs.get_members_of_club(club_id)), 200


@app.route("/api/users/<int:user_id>/clubs", methods=["GET"])
def get_user_clubs_route(user_id):
    if users.get_user_by_id(user_id) is None:
        return not_found("User not found")
    return jsonify(clubs.get_clubs_for_user(user_id)), 200


@app.route("/api/users/<int:user_id>/clubs/<int:club_id>", methods=["POST"])
def join_club_route(user_id, club_id):
    if users.get_user_by_id(user_id) is None:
        return not_found("User not found")
    if clubs.get_club_by_id(club_id) is None:
        return not_found("Club not found")
    joined_new_row = clubs.join_club(user_id, club_id)
    message = "Joined club" if joined_new_row else "Already a member of this club"
    return jsonify({"message": message}), 200


@app.route("/api/users/<int:user_id>/clubs/<int:club_id>", methods=["DELETE"])
def leave_club_route(user_id, club_id):
    clubs.leave_club(user_id, club_id)
    return jsonify({"message": "Left club"}), 200


# Club Manager (ISA relation)

@app.route("/api/users/<int:user_id>/manager", methods=["POST"])
def make_manager_route(user_id):
    """{ "startDate": "YYYY-MM-DD" (optional), "roles": ["social_media", ...] (optional) }"""
    if users.get_user_by_id(user_id) is None:
        return not_found("User not found")

    data = request.get_json() or {}
    clubs.make_club_manager(user_id, data.get("startDate"))
    for role in data.get("roles", []):
        clubs.set_manager_role(user_id, role)

    return jsonify({"message": "User is now a Club_Manager", "roles": clubs.get_manager_roles(user_id)}), 201


@app.route("/api/users/<int:user_id>/manager/roles", methods=["GET"])
def get_manager_roles_route(user_id):
    if not clubs.is_club_manager(user_id):
        return not_found("This user is not a Club_Manager")
    return jsonify({"roles": clubs.get_manager_roles(user_id)}), 200


@app.route("/api/clubs/<int:club_id>/managers", methods=["GET"])
def get_club_managers_route(club_id):
    return jsonify(clubs.get_managers_of_club(club_id)), 200


@app.route("/api/clubs/<int:club_id>/managers/<int:user_id>", methods=["POST"])
def assign_manager_route(club_id, user_id):
    if not clubs.is_club_manager(user_id):
        return bad_request("User must be a Club_Manager first (POST /api/users/<id>/manager)")
    clubs.assign_manager_to_club(club_id, user_id)
    return jsonify({"message": "Manager assigned to club"}), 200


@app.route("/api/users/<int:user_id>/managed-clubs", methods=["GET"])
def get_managed_clubs_route(user_id):
    return jsonify(clubs.get_clubs_managed_by(user_id)), 200


# Club Information Request

@app.route("/api/club-requests", methods=["POST"])
def submit_club_request_route():
    data = request.get_json()
    user_id, proposed_name = data.get("userId"), data.get("proposedClubName")
    if not user_id or not proposed_name:
        return bad_request("userId and proposedClubName are required")
    new_id = clubs.submit_club_request(
        user_id, proposed_name, data.get("intention"), data.get("activities")
    )
    return jsonify({"message": "Request submitted", "requestId": new_id}), 201


@app.route("/api/club-requests", methods=["GET"])
def list_club_requests_route():
    return jsonify(clubs.get_club_requests(status=request.args.get("status"))), 200


@app.route("/api/club-requests/<int:request_id>/review", methods=["POST"])
def review_club_request_route(request_id):
    data = request.get_json()
    admin_id, approve = data.get("adminId"), data.get("approve")
    if not admin_id or approve is None:
        return bad_request("adminId and approve (true/false) are required")
    clubs.review_club_request(request_id, admin_id, approve)
    return jsonify({"message": "Request reviewed"}), 200


# BROADCASTS (EventUpdate / Poll / Announcement / Notifications)
@app.route("/api/clubs/<int:club_id>/events", methods=["POST"])
def create_event_route(club_id):
    data = request.get_json()
    author_id = data.get("authorUserId")
    if not author_id:
        return bad_request("authorUserId is required")
    broadcast_id = broadcasts.create_event_update(
        club_id, author_id, data.get("eventDate"), data.get("eventLocation"), data.get("eventDescription")
    )
    broadcasts.notify_club_members(club_id, broadcast_id, f"New event update in {clubs.get_club_by_id(club_id)['clubName']}")
    return jsonify({"message": "Event created", "broadcastId": broadcast_id}), 201


@app.route("/api/clubs/<int:club_id>/polls", methods=["POST"])
def create_poll_route(club_id):
    data = request.get_json()
    author_id = data.get("authorUserId")
    if not author_id or not data.get("pollQuestion"):
        return bad_request("authorUserId and pollQuestion are required")
    broadcast_id = broadcasts.create_poll(club_id, author_id, data["pollQuestion"], data.get("pollCloseDate"))
    broadcasts.notify_club_members(club_id, broadcast_id, f"New poll in {clubs.get_club_by_id(club_id)['clubName']}")
    return jsonify({"message": "Poll created", "broadcastId": broadcast_id}), 201


@app.route("/api/clubs/<int:club_id>/announcements", methods=["POST"])
def create_announcement_route(club_id):
    data = request.get_json()
    author_id = data.get("authorUserId")
    if not author_id or not data.get("announcementText"):
        return bad_request("authorUserId and announcementText are required")
    broadcast_id = broadcasts.create_announcement(club_id, author_id, data["announcementText"])
    broadcasts.notify_club_members(club_id, broadcast_id, f"New announcement in {clubs.get_club_by_id(club_id)['clubName']}")
    return jsonify({"message": "Announcement created", "broadcastId": broadcast_id}), 201


@app.route("/api/clubs/<int:club_id>/feed", methods=["GET"])
def get_club_feed_route(club_id):
    """Combined, newest-first feed of events + polls + announcements -- powers the dashboard."""
    return jsonify(broadcasts.get_feed_for_club(club_id)), 200


@app.route("/api/users/<int:user_id>/notifications", methods=["GET"])
def get_notifications_route(user_id):
    unread_only = request.args.get("unread") == "true"
    return jsonify(broadcasts.get_notifications_for_user(user_id, unread_only)), 200


@app.route("/api/notifications/<int:notification_id>/read", methods=["POST"])
def mark_notification_read_route(notification_id):
    broadcasts.mark_notification_read(notification_id)
    return jsonify({"message": "Notification marked as read"}), 200


# POSTS + INTERACTIONS
@app.route("/api/posts", methods=["GET"])
def list_posts_route():
    return jsonify(social.get_all_posts()), 200


@app.route("/api/posts", methods=["POST"])
def create_post_route():
    data = request.get_json()
    author_id, content = data.get("authorUserId"), data.get("content")
    if not author_id or not content:
        return bad_request("authorUserId and content are required")
    new_id = social.create_post(author_id, content)
    return jsonify({"message": "Post created", "postId": new_id}), 201


@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post_route(post_id):
    post = social.get_post_by_id(post_id)
    if post is None:
        return not_found("Post not found")
    return jsonify(post), 200


@app.route("/api/posts/<int:post_id>/interactions", methods=["GET"])
def get_post_interactions_route(post_id):
    return jsonify(social.get_interactions_for_post(post_id)), 200


@app.route("/api/interactions", methods=["POST"])
def create_interaction_route():
    """
    { "interactionType": "like"|"comment"|"share"|"tag", "initiatorUserId",
      "content" (optional), "targetPostId" (for like/comment/tag),
      "recipientUserId" (for share) }
    """
    data = request.get_json()
    try:
        new_id = social.create_interaction(
            interaction_type=data.get("interactionType"),
            initiator_user_id=data.get("initiatorUserId"),
            content=data.get("content"),
            target_post_id=data.get("targetPostId"),
            recipient_user_id=data.get("recipientUserId"),
        )
    except ValueError as e:
        return bad_request(str(e))
    return jsonify({"message": "Interaction recorded", "interactionId": new_id}), 201


@app.route("/api/users/<int:user_id>/interactions", methods=["GET"])
def get_user_interactions_route(user_id):
    return jsonify(social.get_interactions_by_user(user_id)), 200


@app.route("/api/users/<int:user_id>/shares", methods=["GET"])
def get_user_shares_route(user_id):
    return jsonify(social.get_shares_received_by_user(user_id)), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)