const API_BASE_URL = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");
  const createClubForm = document.getElementById("createClubForm");
  const settingsForm = document.getElementById("settingsForm");

  if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const username = document.getElementById("loginUsername").value.trim();
      const password = document.getElementById("loginPassword").value;

      try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (!response.ok) {
          // response.ok is false for 4xx/5xx statuses, e.g. wrong password
          alert(data.error || "Login failed. Please try again.");
          return;
        }

        // Save the logged-in user's info so other pages (like settings.html)
        // can use it. We keep this in localStorage just for convenience of
        // remembering who's logged in on this browser -- the *source of truth*
        // for the account itself is now the MySQL database, not localStorage.
        localStorage.setItem("clubtimeUser", JSON.stringify(data.user));

        window.location.href = "index.html";
      } catch (error) {
        // This branch runs if the fetch itself failed, e.g. the Flask
        // server isn't running or CORS is blocking it.
        console.error("Login request failed:", error);
        alert("Could not reach the server. Is the Flask backend running on port 5000?");
      }
    });
  }

  if (signupForm) {
    signupForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const fullName = document.getElementById("signupName").value.trim();
      const username = document.getElementById("signupUsername").value.trim();
      const dob = document.getElementById("signupDob").value; // "YYYY-MM-DD" from <input type="date">
      const password = document.getElementById("signupPassword").value;

      // signup.html only has one "Name" field, but the users table stores
      // firstName and lastName separately. Split on the first space so
      // "Larry Test" becomes firstName "Larry", lastName "Test".
      // If there's no space (just one word), lastName is left blank.
      const spaceIndex = fullName.indexOf(" ");
      const firstName = spaceIndex === -1 ? fullName : fullName.slice(0, spaceIndex);
      const lastName = spaceIndex === -1 ? "" : fullName.slice(spaceIndex + 1);

      try {
        const response = await fetch(`${API_BASE_URL}/api/signup`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ firstName, lastName, username, dob, password }),
        });

        const data = await response.json();

        if (!response.ok) {
          alert(data.error || "Signup failed. Please try again.");
          return;
        }

        alert("Account created! You can now log in.");
        window.location.href = "login.html";
      } catch (error) {
        console.error("Signup request failed:", error);
        alert("Could not reach the server. Is the Flask backend running on port 5000?");
      }
    });
  }

  if (createClubForm) {
    createClubForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const clubName = document.getElementById("newClubName").value.trim();

      if (!clubName) {
        return;
      }

      const savedClubs = JSON.parse(localStorage.getItem("clubtimeClubs") || "[]");

      if (!savedClubs.includes(clubName)) {
        savedClubs.push(clubName);
        localStorage.setItem("clubtimeClubs", JSON.stringify(savedClubs));
      }

      const savedPosts = JSON.parse(localStorage.getItem("clubtimePosts") || "{}");

      if (!savedPosts[clubName]) {
        savedPosts[clubName] = [
          {
            type: "announcement",
            title: `Welcome to ${clubName}`,
            message: "This club was just created. Add your first announcement from the dashboard.",
            date: "Posted just now"
          }
        ];
        localStorage.setItem("clubtimePosts", JSON.stringify(savedPosts));
      }

      localStorage.setItem("clubtimeSelectedClub", clubName);
      alert(`${clubName} was created in this frontend demo.`);
      window.location.href = "index.html";
    });
  }

  if (settingsForm) {
    const savedName = localStorage.getItem("clubtimeName");

    if (savedName) {
      document.getElementById("settingsName").value = savedName;
    }

    settingsForm.addEventListener("submit", function (event) {
      event.preventDefault();

      localStorage.setItem(
        "clubtimeName",
        document.getElementById("settingsName").value.trim()
      );

      localStorage.setItem(
        "clubtimeSelectedClub",
        document.getElementById("settingsClub").value
      );

      localStorage.setItem(
        "clubtimeRole",
        document.getElementById("settingsRole").value
      );

      alert("Settings saved in your browser.");
    });
  }

  const clubNameHeading = document.getElementById("clubName");
  const joinButton = document.getElementById("joinButton");
  const usersButton = document.getElementById("usersButton");
  const usersList = document.getElementById("usersList");
  const usersArrow = document.getElementById("usersArrow");
  const announcementContainer = document.getElementById("announcementContainer");
  const addPostButton = document.getElementById("addPostButton");
  const addUsersButton = document.getElementById("addUsersButton");
  const addUsersDialog = document.getElementById("addUsersDialog");
  const addUsersForm = document.getElementById("addUsersForm");

  const defaultClubPosts = {
    "Coding Club": [
      {
        type: "announcement",
        title: "Welcome to Coding Club",
        message: "Our first meeting is Friday at 4:00 PM in the Student Union.",
        date: "Posted July 18"
      },
      {
        type: "poll",
        title: "What should our next workshop cover?",
        options: ["Web Development", "Mobile App Development", "Artificial Intelligence"]
      },
      {
        type: "announcement",
        title: "Officer Applications Are Open",
        message: "Applications for club officer positions are due July 25.",
        date: "Posted July 16"
      },
      {
        type: "poll",
        title: "Which programming language should we practice?",
        options: ["Java", "Python", "JavaScript"]
      }
    ],
    "Art Club": [
      {
        type: "announcement",
        title: "Watercolor Night",
        message: "Bring your watercolor supplies to Tuesday's painting session in Art Room 204.",
        date: "Posted July 17"
      },
      {
        type: "poll",
        title: "What should our next art session focus on?",
        options: ["Portrait Drawing", "Landscape Painting", "Clay Sculpting"]
      },
      {
        type: "announcement",
        title: "Campus Art Show",
        message: "Submit up to two pieces for the fall campus art show by August 2.",
        date: "Posted July 14"
      }
    ],
    "Photography Club": [
      {
        type: "announcement",
        title: "Golden Hour Photo Walk",
        message: "Meet outside the library at 6:30 PM on Saturday for a sunset photo walk.",
        date: "Posted July 18"
      },
      {
        type: "poll",
        title: "Where should our next photo trip be?",
        options: ["Downtown San Jose", "Santa Cruz Beach", "Japanese Friendship Garden"]
      },
      {
        type: "announcement",
        title: "Photo Contest Theme",
        message: "This month's contest theme is Patterns in Everyday Life.",
        date: "Posted July 12"
      }
    ],
    "Book Club": [
      {
        type: "announcement",
        title: "July Book Discussion",
        message: "We will discuss the final five chapters at Thursday's meeting.",
        date: "Posted July 18"
      },
      {
        type: "poll",
        title: "Choose our next genre",
        options: ["Mystery", "Fantasy", "Historical Fiction"]
      },
      {
        type: "announcement",
        title: "Bring a Recommendation",
        message: "Each member should bring one book recommendation for the next reading list.",
        date: "Posted July 15"
      }
    ],
    "Music Club": [
      {
        type: "announcement",
        title: "Open Mic Rehearsal",
        message: "Rehearsal begins Wednesday at 5:00 PM in the music building.",
        date: "Posted July 18"
      },
      {
        type: "poll",
        title: "What should be our next jam-session theme?",
        options: ["Bollywood", "Pop Classics", "Acoustic Covers"]
      },
      {
        type: "announcement",
        title: "Instrument Sign-Up",
        message: "Add your name and instrument to the sign-up sheet before Friday.",
        date: "Posted July 13"
      }
    ]
  };

  function loadAllClubPosts() {
    const savedPosts = JSON.parse(localStorage.getItem("clubtimePosts") || "{}");

    Object.keys(defaultClubPosts).forEach(function (clubName) {
      if (!savedPosts[clubName]) {
        savedPosts[clubName] = defaultClubPosts[clubName];
      }
    });

    localStorage.setItem("clubtimePosts", JSON.stringify(savedPosts));
    return savedPosts;
  }

  let allClubPosts = loadAllClubPosts();
  let currentClub = localStorage.getItem("clubtimeSelectedClub") || "Coding Club";

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function renderPosts(clubName) {
    if (!announcementContainer) {
      return;
    }

    const posts = allClubPosts[clubName] || [];
    announcementContainer.innerHTML = "";

    if (posts.length === 0) {
      announcementContainer.innerHTML = `
        <article class="post-card announcement-card">
          <span class="post-label announcement-label">Announcement</span>
          <h3>No posts yet</h3>
          <p>This club does not have any announcements or polls yet.</p>
        </article>
      `;
      return;
    }

    posts.forEach(function (post, postIndex) {
      const article = document.createElement("article");

      if (post.type === "poll") {
        article.className = "post-card poll-card";
        const pollName = `poll-${clubName.replace(/[^a-z0-9]/gi, "-")}-${postIndex}`;
        const optionsHtml = post.options
          .map(function (option) {
            return `
              <label class="poll-option">
                <input type="radio" name="${pollName}" value="${escapeHtml(option)}">
                ${escapeHtml(option)}
              </label>
            `;
          })
          .join("");

        article.innerHTML = `
          <span class="post-label poll-label">Poll</span>
          <h3>${escapeHtml(post.title)}</h3>
          ${optionsHtml}
          <button class="vote-button" type="button">Submit Vote</button>
        `;
      } else {
        article.className = "post-card announcement-card";
        article.innerHTML = `
          <span class="post-label announcement-label">Announcement</span>
          <h3>${escapeHtml(post.title)}</h3>
          <p>${escapeHtml(post.message)}</p>
          <p class="post-date">${escapeHtml(post.date || "Posted recently")}</p>
        `;
      }

      announcementContainer.appendChild(article);
    });

    announcementContainer.scrollTop = 0;
  }

  function selectClub(clubName, selectedButton) {
    currentClub = clubName;
    localStorage.setItem("clubtimeSelectedClub", currentClub);

    document.querySelectorAll(".club-button").forEach(function (button) {
      button.classList.remove("active");
    });

    if (selectedButton) {
      selectedButton.classList.add("active");
    }

    if (clubNameHeading) {
      clubNameHeading.textContent = currentClub;
    }

    if (joinButton) {
      joinButton.textContent = "Join Club";
      joinButton.classList.remove("joined");
    }

    renderPosts(currentClub);
  }

  if (clubNameHeading) {
    const savedClubs = JSON.parse(localStorage.getItem("clubtimeClubs") || "[]");
    const clubList = document.querySelector(".club-list");

    savedClubs.forEach(function (club) {
      if (!document.querySelector(`.club-button[data-club="${CSS.escape(club)}"]`)) {
        const button = document.createElement("button");
        button.className = "club-button";
        button.dataset.club = club;
        button.textContent = club;
        clubList.appendChild(button);
      }

      if (!allClubPosts[club]) {
        allClubPosts[club] = [
          {
            type: "announcement",
            title: `Welcome to ${club}`,
            message: "This club has no additional posts yet. Use Add Post to create one.",
            date: "Posted recently"
          }
        ];
      }
    });

    localStorage.setItem("clubtimePosts", JSON.stringify(allClubPosts));

    const availableButtons = document.querySelectorAll(".club-button");
    let selectedButton = Array.from(availableButtons).find(function (button) {
      return button.dataset.club === currentClub;
    });

    if (!selectedButton && availableButtons.length > 0) {
      selectedButton = availableButtons[0];
      currentClub = selectedButton.dataset.club;
    }

    availableButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        selectClub(button.dataset.club, button);
      });
    });

    if (selectedButton) {
      selectClub(currentClub, selectedButton);
    }
  }

  if (joinButton) {
    joinButton.addEventListener("click", function () {
      const joined = joinButton.classList.toggle("joined");
      joinButton.textContent = joined ? "Joined" : "Join Club";
    });
  }

  if (usersButton && usersList && usersArrow) {
    usersButton.addEventListener("click", function () {
      usersList.classList.toggle("hidden");
      usersArrow.textContent = usersList.classList.contains("hidden") ? "▶" : "▼";
    });
  }

  if (announcementContainer) {
    announcementContainer.addEventListener("click", function (event) {
      const button = event.target.closest(".vote-button");

      if (!button) {
        return;
      }

      const pollCard = button.closest(".poll-card");
      const selected = pollCard.querySelector('input[type="radio"]:checked');

      if (!selected) {
        alert("Please select an option before voting.");
        return;
      }

      alert(`Your vote for "${selected.value}" was submitted for ${currentClub}.`);
      button.textContent = "Vote Submitted";
      button.disabled = true;
    });
  }

  if (addPostButton && announcementContainer) {
    addPostButton.addEventListener("click", function () {
      const title = prompt(`Announcement title for ${currentClub}:`);

      if (!title) {
        return;
      }

      const message = prompt("Announcement message:");

      if (!message) {
        return;
      }

      if (!allClubPosts[currentClub]) {
        allClubPosts[currentClub] = [];
      }

      allClubPosts[currentClub].unshift({
        type: "announcement",
        title: title.trim(),
        message: message.trim(),
        date: "Posted just now"
      });

      localStorage.setItem("clubtimePosts", JSON.stringify(allClubPosts));
      renderPosts(currentClub);
    });
  }

  if (addUsersButton && addUsersDialog) {
    addUsersButton.addEventListener("click", function () {
      addUsersDialog.showModal();
    });
  }

  if (addUsersForm && usersList) {
    addUsersForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const nameInput = document.getElementById("newUserName");
      const roleInput = document.getElementById("newUserRole");
      const name = nameInput.value.trim();

      if (!name) {
        return;
      }

      const initials = name
        .split(" ")
        .map(function (word) {
          return word[0];
        })
        .join("")
        .slice(0, 2)
        .toUpperCase();

      const userCard = document.createElement("div");
      userCard.className = "user-card";
      userCard.innerHTML = `
        <div class="user-avatar"></div>
        <div>
          <strong></strong>
          <p></p>
        </div>
      `;

      userCard.querySelector(".user-avatar").textContent = initials;
      userCard.querySelector("strong").textContent = name;
      userCard.querySelector("p").textContent = roleInput.value;

      usersList.appendChild(userCard);
      nameInput.value = "";
      roleInput.value = "Member";
      addUsersDialog.close();
    });
  }
});