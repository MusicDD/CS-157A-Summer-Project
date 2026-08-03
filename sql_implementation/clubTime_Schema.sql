
-- ClubTime Database Schema
-- CS157A Final Project

 
DROP DATABASE IF EXISTS clubtime;
CREATE DATABASE clubtime;
USE clubtime;


CREATE TABLE Admin (
    adminId     INT AUTO_INCREMENT PRIMARY KEY,
    firstName   VARCHAR(50)  NOT NULL,
    lastName    VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE
);
 
CREATE TABLE Clubs (
    clubId          INT AUTO_INCREMENT PRIMARY KEY,
    clubName        VARCHAR(100) NOT NULL,
    clubStatus      ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    clubFocus       VARCHAR(100),
    lastActivityDate DATE
);

CREATE TABLE User (
    userId          INT AUTO_INCREMENT PRIMARY KEY,
    firstName       VARCHAR(50)  NOT NULL,
    lastName        VARCHAR(50)  NOT NULL,
    DoB             DATE         NOT NULL,
    joinDate        DATE         NOT NULL,
    passwordHash    VARCHAR(255) NOT NULL,
    bannedByAdminId INT NULL,
    FOREIGN KEY (bannedByAdminId) REFERENCES Admin(adminId)
        ON DELETE SET NULL
);
 

CREATE TABLE UserEmail (
    userId  INT NOT NULL,
    email   VARCHAR(100) NOT NULL,
    PRIMARY KEY (userId, email),
    FOREIGN KEY (userId) REFERENCES User(userId)
        ON DELETE CASCADE
);
 
CREATE TABLE UserPhone (
    userId  INT NOT NULL,
    phone   VARCHAR(20) NOT NULL,
    PRIMARY KEY (userId, phone),
    FOREIGN KEY (userId) REFERENCES User(userId)
        ON DELETE CASCADE
);
 

 
CREATE TABLE Club_Manager (
    userId      INT NOT NULL PRIMARY KEY,
    startDate   DATE NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(userId)
        ON DELETE CASCADE
);
 
CREATE TABLE SocialMediaManager (
    userId  INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (userId) REFERENCES Club_Manager(userId)
        ON DELETE CASCADE
);
 
CREATE TABLE EventCoordinator (
    userId  INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (userId) REFERENCES Club_Manager(userId)
        ON DELETE CASCADE
);
 
CREATE TABLE ChatModerator (
    userId  INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (userId) REFERENCES Club_Manager(userId)
        ON DELETE CASCADE
);
 
 
CREATE TABLE ClubFormationRequest (
    requestId               INT AUTO_INCREMENT PRIMARY KEY,
    userId                  INT NOT NULL,
    reviewedByAdminId       INT NULL,
    proposedClubName        VARCHAR(100) NOT NULL,
    club_Intention          VARCHAR(255),
    proposedClubActivities  VARCHAR(255),
    status                  ENUM('pending', 'approved', 'denied') NOT NULL DEFAULT 'pending',
    requestDate             DATE NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(userId)
        ON DELETE CASCADE,
    FOREIGN KEY (reviewedByAdminId) REFERENCES Admin(adminId)
        ON DELETE SET NULL
);

 
CREATE TABLE ClubManagement (
    clubId  INT NOT NULL,
    userId  INT NOT NULL,
    PRIMARY KEY (clubId, userId),
    FOREIGN KEY (clubId) REFERENCES Clubs(clubId)
        ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES Club_Manager(userId)
        ON DELETE CASCADE
);
 
CREATE TABLE Membership (
    userId      INT NOT NULL,
    clubId      INT NOT NULL,
    dateJoined  DATE NOT NULL,
    PRIMARY KEY (userId, clubId),
    FOREIGN KEY (userId) REFERENCES User(userId)
        ON DELETE CASCADE,
    FOREIGN KEY (clubId) REFERENCES Clubs(clubId)
        ON DELETE CASCADE
);
 
CREATE TABLE AdminManagesClub (
    adminId INT NOT NULL,
    clubId  INT NOT NULL,
    PRIMARY KEY (adminId, clubId),
    FOREIGN KEY (adminId) REFERENCES Admin(adminId)
        ON DELETE CASCADE,
    FOREIGN KEY (clubId) REFERENCES Clubs(clubId)
        ON DELETE CASCADE
);


CREATE TABLE Broadcast (
    broadcastId         INT AUTO_INCREMENT PRIMARY KEY,
    broadcastTimestamp  DATETIME NOT NULL,
    clubId              INT NOT NULL,
    FOREIGN KEY (clubId) REFERENCES Clubs(clubId)
        ON DELETE CASCADE
);
 
CREATE TABLE BroadcastAuthors (
    broadcastId INT NOT NULL,
    userId      INT NOT NULL,
    PRIMARY KEY (broadcastId, userId),
    FOREIGN KEY (broadcastId) REFERENCES Broadcast(broadcastId)
        ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES Club_Manager(userId)
        ON DELETE CASCADE
);
 
CREATE TABLE EventUpdate (
    broadcastId     INT NOT NULL PRIMARY KEY,
    eventDate       DATE,
    eventLocation   VARCHAR(100),
    eventDescription VARCHAR(255),
    FOREIGN KEY (broadcastId) REFERENCES Broadcast(broadcastId)
        ON DELETE CASCADE
);
 
CREATE TABLE Poll (
    broadcastId     INT NOT NULL PRIMARY KEY,
    pollQuestion    VARCHAR(255) NOT NULL,
    pollCloseDate   DATE,
    FOREIGN KEY (broadcastId) REFERENCES Broadcast(broadcastId)
        ON DELETE CASCADE
);
 
CREATE TABLE Announcement (
    broadcastId       INT NOT NULL PRIMARY KEY,
    announcementText  VARCHAR(500) NOT NULL,
    FOREIGN KEY (broadcastId) REFERENCES Broadcast(broadcastId)
        ON DELETE CASCADE
);
 

 
CREATE TABLE Notification (
    notificationId  INT AUTO_INCREMENT PRIMARY KEY,
    content         VARCHAR(255) NOT NULL,
    isRead          BOOLEAN NOT NULL DEFAULT FALSE,
    sentTimestamp   DATETIME NOT NULL,
    broadcastId     INT NOT NULL,
    userId          INT NOT NULL,
    FOREIGN KEY (broadcastId) REFERENCES Broadcast(broadcastId)
        ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES User(userId)
        ON DELETE CASCADE
);
 
 
CREATE TABLE PostThread (
    postId          INT AUTO_INCREMENT PRIMARY KEY,
    content         VARCHAR(500) NOT NULL,
    createdDate     DATE NOT NULL,
    authorUserId    INT NOT NULL,
    FOREIGN KEY (authorUserId) REFERENCES User(userId)
        ON DELETE CASCADE
);
 

CREATE TABLE Interaction (
    interactionId       INT AUTO_INCREMENT PRIMARY KEY,
    interactionType     ENUM('like', 'comment', 'share', 'tag') NOT NULL,
    content             VARCHAR(255),
    timestamp           DATETIME NOT NULL,
    initiatorUserId     INT NOT NULL,
    targetPostId        INT NULL,
    recipientUserId     INT NULL,
    FOREIGN KEY (initiatorUserId) REFERENCES User(userId)
        ON DELETE CASCADE,
    FOREIGN KEY (targetPostId) REFERENCES PostThread(postId)
        ON DELETE CASCADE,
    FOREIGN KEY (recipientUserId) REFERENCES User(userId)
        ON DELETE CASCADE,
    CHECK (
        (targetPostId IS NOT NULL AND recipientUserId IS NULL)
        OR (targetPostId IS NULL AND recipientUserId IS NOT NULL)
    )
);
 