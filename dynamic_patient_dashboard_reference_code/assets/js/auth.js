// auth.js

// Function to handle user login
async function handleLogin(event) {
  event.preventDefault();

  const identifier = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  // Fix: Get role from active button instead of select element
  const role = document
    .querySelector(".role-btn.active")
    .getAttribute("data-role");

  try {
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        identifier,
        password,
        role,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      // Store user data and token in localStorage
      const userData = {
        id: data.user.id,
        name: data.user.name,
        email: data.user.email,
        role: data.user.role,
      };

      localStorage.setItem("user", JSON.stringify(userData));
      localStorage.setItem("token", data.token);

      // Fix: Update redirect paths to match your file structure
      if (role === "patient") {
        window.location.href = "../pages/patient-dashboard.html";
      } else {
        window.location.href = "../pages/admin-dashboard.html";
      }
    } else {
      // Handle login error
      const errorDisplay = document.getElementById("error-message");
      if (errorDisplay) {
        errorDisplay.textContent =
          data.detail || "Login failed. Please try again.";
        errorDisplay.style.display = "block";
      }
    }
  } catch (error) {
    console.error("Login error:", error);
    const errorDisplay = document.getElementById("error-message");
    if (errorDisplay) {
      errorDisplay.textContent = "An error occurred. Please try again later.";
      errorDisplay.style.display = "block";
    }
  }
}

// Function to check if user is logged in and return clean user data
function checkAuth() {
  const userStr = localStorage.getItem("user");
  const token = localStorage.getItem("token");

  if (!userStr || !token) {
    window.location.href = "../index.html";
    return null;
  }

  try {
    // Parse and validate user data
    const userData = JSON.parse(userStr);
    if (!userData.name || !userData.role) {
      // Invalid user data, force re-login
      handleLogout();
      return null;
    }
    return userData;
  } catch (e) {
    // Invalid JSON in localStorage, force re-login
    handleLogout();
    return null;
  }
}

// Function to handle logout
function handleLogout() {
  localStorage.removeItem("user");
  localStorage.removeItem("token");
  window.location.href = "../index.html";
}

// Add event listeners when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Add login form submit handler
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }

  // Add logout handler
  const logoutLink = document.querySelector('a[href="../index.html"]');
  if (logoutLink) {
    logoutLink.addEventListener("click", function (e) {
      e.preventDefault();
      handleLogout();
    });
  }
});
