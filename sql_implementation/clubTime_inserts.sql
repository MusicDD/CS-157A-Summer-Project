-- ClubTime! Inserts; meant to be ran AFTER clubTime_Schema has been processed 

USE clubtime;
 

INSERT INTO Admin (adminId, firstName, lastName, email) VALUES
(1, 'Priya', 'Nair', 'priya.nair@sjsu.edu'),
(2, 'Marcus', 'Lee', 'marcus.lee@sjsu.edu');
 

INSERT INTO Clubs (clubId, clubName, clubStatus, clubFocus, lastActivityDate) VALUES
(1, 'AI & Robotics Society', 'active', 'Technology', '2026-07-28'),
(2, 'Culinary Explorers', 'active', 'Food & Culture', '2026-07-30'),
(3, 'Chess Collective', 'active', 'Games & Strategy', '2026-07-25'),
(4, 'Retired Film Club', 'inactive', 'Film', '2023-05-10');
 

INSERT INTO User (userId, firstName, lastName, DoB, joinDate, passwordHash, bannedByAdminId) VALUES
(1, 'Ara', 'Kumar', '2004-03-12', '2025-08-20', 'hash_a1b2c3', NULL),
(2, 'Hikaru', 'Park',        '2003-11-02', '2025-08-21', 'hash_d4e5f6', NULL),
(3, 'Hinata', 'Shoyo',       '2004-06-19', '2025-09-01', 'hash_g7h8i9', NULL),
(4, 'Malik', 'Thompson',    '2002-01-30', '2025-09-05', 'hash_j1k2l3', NULL),
(5, 'Wei',   'Zhang',       '2003-08-14', '2025-09-10', 'hash_m4n5o6', NULL),
(6, 'Jonas', 'Becker',      '2001-12-25', '2024-01-15', 'hash_p7q8r9', 1);
 

INSERT INTO UserEmail (userId, email) VALUES
(1, 'ara@sjsu.edu'), (1, 'ara.personal@gmail.com'),
(2, 'hikaru@sjsu.edu'),
(3, 'hinata@sjsu.edu'), (3, 'hinata.shoyo@gmail.com'),
(4, 'malik@sjsu.edu'),
(5, 'wei@sjsu.edu'),
(6, 'jonas@sjsu.edu');
 
INSERT INTO UserPhone (userId, phone) VALUES
(1, '408-555-0101'),
(2, '408-555-0102'),
(3, '408-555-0103'), (3, '650-555-9999'),
(5, '408-555-0105');
 

INSERT INTO Club_Manager (userId, startDate) VALUES
(1, '2025-09-01'),
(2, '2025-09-01'),
(3, '2025-09-15'),
(4, '2025-10-01');
 

INSERT INTO SocialMediaManager (userId) VALUES (1), (3);
INSERT INTO EventCoordinator (userId) VALUES (1), (2);
INSERT INTO ChatModerator (userId) VALUES (4);
 

INSERT INTO ClubFormationRequest
    (requestId, userId, reviewedByAdminId, proposedClubName, club_Intention, proposedClubActivities, status, requestDate) VALUES
(1, 5, 1, 'Data Science Guild', 'Build a community around applied ML', 'Workshops, Kaggle competitions', 'approved', '2026-07-01'),
(2, 6, 2, 'Late Night Gaming', 'Casual esports meetups', 'LAN parties, tournaments', 'denied', '2026-07-03'),
(3, 4, NULL, 'Outdoor Adventure Club', 'Weekend hiking trips', 'Hikes, camping trips', 'pending', '2026-07-29');
 

INSERT INTO Membership (userId, clubId, dateJoined) VALUES
(1, 1, '2025-09-01'),
(1, 2, '2025-09-10'),
(2, 1, '2025-09-02'),
(3, 2, '2025-09-15'),
(3, 3, '2025-09-16'),
(4, 3, '2025-10-01'),
(5, 1, '2025-09-20'),
(6, 4, '2024-01-16');
 

INSERT INTO ClubManagement (clubId, userId) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4);


INSERT INTO AdminManagesClub (adminId, clubId) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4);
 

INSERT INTO Broadcast (broadcastId, broadcastTimestamp, clubId) VALUES
(1, '2026-07-20 10:00:00', 1),
(2, '2026-07-22 14:30:00', 1),
(3, '2026-07-25 09:15:00', 2),
(4, '2026-07-27 18:00:00', 3);
 
INSERT INTO BroadcastAuthors (broadcastId, userId) VALUES
(1, 1), (2, 2), (3, 3), (4, 4);
 
INSERT INTO EventUpdate (broadcastId, eventDate, eventLocation, eventDescription) VALUES
(1, '2026-08-01', 'Engineering Bldg Rm 189', 'Kickoff meeting for new ML Club teams');
 
INSERT INTO Poll (broadcastId, pollQuestion, pollCloseDate) VALUES
(2, 'What should our next workshop topic be?', '2026-08-05');
 
INSERT INTO Announcement (broadcastId, announcementText) VALUES
(3, 'Culinary Explorers will be hosting a potluck next Friday. Sign up on the shared sheet! Forget or you might be executed! JK JK...unless'),
(4, 'Chess Collective tournament bracket has been posted, check your matchups.');
 

INSERT INTO Notification (notificationId, content, isRead, sentTimestamp, broadcastId, userId) VALUES
(1, 'New event update in ML CLub', TRUE,  '2026-07-20 10:01:00', 1, 2),
(2, 'New poll in ML Club', FALSE, '2026-07-22 14:31:00', 2, 1),
(3, 'New announcement in Culinary Explorers', FALSE, '2026-07-25 09:16:00', 3, 1),
(4, 'New announcement in Chess Collective', TRUE,  '2026-07-27 18:01:00', 4, 3);
 

INSERT INTO PostThread (postId, content, createdDate, authorUserId) VALUES
(1, 'Anyone else excited for the Black Belt tournament LOL?', '2026-07-21', 1),
(2, 'Looking for teammates for the Kaggle competition!', '2026-07-23', 5),
(3, 'Potluck dish sign-up thread', '2026-07-25', 3);
 


INSERT INTO Interaction (interactionId, interactionType, content, timestamp, initiatorUserId, targetPostId, recipientUserId) VALUES
(1, 'like',    NULL,                              '2026-07-21 11:00:00', 2, 1, NULL),
(2, 'comment', 'Same, can''t wait!!!! RAHHHH',               '2026-07-21 11:05:00', 3, 1, NULL),
(3, 'like',    NULL,                              '2026-07-23 09:00:00', 1, 2, NULL),
(4, 'share',   'You should see this post',         '2026-07-23 09:10:00', 1, NULL, 4),
(5, 'tag',     'Tagging you in this thread',       '2026-07-25 12:00:00', 3, 3, NULL);