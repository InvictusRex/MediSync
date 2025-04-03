// dashboard.js

// Constants
const API_BASE_URL = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", async function () {
  try {
    // Check authentication first
    const userData = checkAuth();
    if (!userData) {
      // checkAuth will handle redirect if needed
      return;
    }

    // Initialize dashboard components
    initializeSystemInfo();
    updateUserInfo(userData);
    await initializeDashboard(userData.id);

    // Add event listeners for interactive elements
    setupEventListeners();
  } catch (error) {
    console.error("Dashboard initialization error:", error);
    showErrorMessage(
      "Failed to initialize dashboard. Please refresh the page."
    );
  }
});

// Check authentication status
function checkAuth() {
  try {
    const userStr = localStorage.getItem("user");
    const token = localStorage.getItem("token");

    if (!userStr || !token) {
      redirectToLogin();
      return null;
    }

    const userData = JSON.parse(userStr);
    if (!userData.name || !userData.id || !userData.role) {
      redirectToLogin();
      return null;
    }

    return userData;
  } catch (error) {
    console.error("Auth check error:", error);
    redirectToLogin();
    return null;
  }
}

function redirectToLogin() {
  window.location.href = "../index.html";
}

// Update the system info including timestamp
function initializeSystemInfo() {
  function updateSystemInfo() {
    const now = new Date();
    const timestamp = now
      .toISOString()
      .replace("T", " ")
      .replace(/\.\d{3}Z$/, " UTC");

    const datetimeElement = document.getElementById("datetime");
    if (datetimeElement) {
      datetimeElement.textContent = timestamp;
    }
  }

  updateSystemInfo();
  setInterval(updateSystemInfo, 1000);
}

// Update user information in the sidebar
function updateUserInfo(userData) {
  if (!userData?.name) {
    redirectToLogin();
    return;
  }

  const elements = {
    userInitial: userData.name[0].toUpperCase(),
    userName: userData.name,
    patientId: `Patient ID: ${userData.id}`,
  };

  Object.entries(elements).forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = value;
    }
  });
}

// Initialize dashboard with data
async function initializeDashboard(userId) {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      throw new Error("Authentication token not found");
    }

    const response = await fetch(
      `${API_BASE_URL}/patient-dashboard/${userId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const dashboardData = await response.json();

    // Update all dashboard components
    updateDashboardComponents(dashboardData);
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    showErrorMessage("Failed to load dashboard data. Please refresh the page.");
  }
}

// Update all dashboard components
function updateDashboardComponents(data) {
  // Update system info
  if (data.system_info) {
    const { timestamp, user_login } = data.system_info;
    updateElement("datetime", timestamp);
    updateElement("userName", user_login);
  }

  // Update appointments
  updateAppointments(data.appointments);

  // Update profile
  if (data.profile) {
    updateProfile(data.profile);
  }

  // Update card counts
  updateCardCount("Upcoming Appointments", data.appointments?.length || 0);
}

// Update appointments section
function updateAppointments(appointments = []) {
  const tbody = document.querySelector(".appointments-table tbody");
  if (!tbody) return;

  tbody.innerHTML = appointments.length
    ? appointments
        .map(
          (apt) => `
      <tr>
        <td>${escapeHtml(apt.doctor_name)}</td>
        <td>${escapeHtml(apt.date)}</td>
        <td>${escapeHtml(apt.status)}</td>
        <td>
          <button class="btn-primary" data-appointment-id="${apt.id}">
            View Details
          </button>
        </td>
      </tr>
    `
        )
        .join("")
    : '<tr><td colspan="4" class="text-center">No upcoming appointments</td></tr>';
}

// Update profile information
function updateProfile(profile) {
  const profileElements = {
    "profile-name": profile.name,
    "profile-age": profile.age,
    "profile-blood": profile.blood_group,
    "profile-medical-history": profile.medical_history,
    "profile-phone": profile.phone,
    "profile-email": profile.email,
  };

  Object.entries(profileElements).forEach(([id, value]) => {
    updateElement(id, value);
  });
}

// Helper function to safely update element content
function updateElement(id, content) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = content;
  }
}

// Update individual card counts
function updateCardCount(title, count) {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    const cardTitle = card.querySelector(".card-title");
    if (cardTitle?.textContent === title) {
      const countElement = card.querySelector(".card-body h2");
      if (countElement) {
        countElement.textContent = count;
      }
    }
  });
}

// Show error message
function showErrorMessage(message) {
  const errorDiv = document.getElementById("error-message");
  if (errorDiv) {
    errorDiv.textContent = message;
    errorDiv.style.display = "block";

    // Auto-hide after 5 seconds
    setTimeout(() => {
      errorDiv.style.display = "none";
    }, 5000);
  }
}

// Theme toggle function
function toggleTheme() {
  const body = document.body;
  const currentTheme = body.getAttribute("data-theme");
  body.setAttribute("data-theme", currentTheme === "dark" ? "" : "dark");
  localStorage.setItem("theme", currentTheme === "dark" ? "light" : "dark");
}

// Setup event listeners
function setupEventListeners() {
  // Modal handlers
  document.querySelectorAll("[data-modal]").forEach((button) => {
    button.addEventListener("click", () => {
      const modalId = button.getAttribute("data-modal");
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.style.display = "flex";
      }
    });
  });

  document.querySelectorAll(".close-modal").forEach((button) => {
    button.addEventListener("click", () => {
      const modal = button.closest(".modal");
      if (modal) {
        modal.style.display = "none";
      }
    });
  });

  // Close modals when clicking outside
  window.addEventListener("click", (event) => {
    if (event.target.classList.contains("modal")) {
      event.target.style.display = "none";
    }
  });
}

// Helper function to escape HTML content
function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
