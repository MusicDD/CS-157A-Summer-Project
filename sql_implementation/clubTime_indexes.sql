Indexes · SQL

-- clubTime! indexes; note: this is meant to be parsed through/ran AFTER processing the schema and the inserts (data input)

USE clubtime;
 
-- User -> banned-by lookups (admin dashboard, moderation queries)
CREATE INDEX idx_user_bannedBy ON User(bannedByAdminId);
 
-- Login lookup by email (since composite PK is userId and email, so a
-- lookup by email alone wouldn't use that index efficiently)
CREATE INDEX idx_useremail_email ON UserEmail(email);
 
-- Club Formation Request: reviewer lookups + status filtering
-- (for instance: "show all pending requests")
CREATE INDEX idx_cfr_userId ON ClubFormationRequest(userId);
CREATE INDEX idx_cfr_reviewedBy ON ClubFormationRequest(reviewedByAdminId);
CREATE INDEX idx_cfr_status ON ClubFormationRequest(status);
 
-- Clubs ->  browsing by name and filtering active/inactive
-- (core "browse clubs" functional requirement)
CREATE INDEX idx_clubs_name ON Clubs(clubName);
CREATE INDEX idx_clubs_status ON Clubs(clubStatus);
 
-- Reverse lookups on junction tables (PK covers one direction,
-- these cover the other. for instance, "clubs a manager oversees")
CREATE INDEX idx_clubmanagement_userId ON ClubManagement(userId);
CREATE INDEX idx_adminmanagesclub_clubId ON AdminManagesClub(clubId);
CREATE INDEX idx_broadcastauthors_userId ON BroadcastAuthors(userId);
 
-- Membership ->  "which clubs is a user in" is covered by the PK
-- (userId, clubId); this covers "who are a club's members"

CREATE INDEX idx_membership_clubId ON Membership(clubId);
 
-- Broadcast: fetching all broadcasts for a given club
CREATE INDEX idx_broadcast_clubId ON Broadcast(clubId);
 
-- Notification: fetching a user's notifications, and unread filtering
CREATE INDEX idx_notification_userId ON Notification(userId);
CREATE INDEX idx_notification_broadcastId ON Notification(broadcastId);
CREATE INDEX idx_notification_isRead ON Notification(isRead);
 
-- PostThread: retrieving all the posts that were posted by a given author
CREATE INDEX idx_postthread_authorUserId ON PostThread(authorUserId);
 
-- Interaction: fetching interactions by the initiating user, by target post,
-- or by recipient (like/comment/tag vs. share lookups)
CREATE INDEX idx_interaction_initiator ON Interaction(initiatorUserId);
CREATE INDEX idx_interaction_targetPost ON Interaction(targetPostId);
CREATE INDEX idx_interaction_recipient ON Interaction(recipientUserId);