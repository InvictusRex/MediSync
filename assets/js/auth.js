document.addEventListener("DOMContentLoaded", function () {
  // Role selection handling
  const roleButtons = document.querySelectorAll(".role-btn");
  const loginForm = document.getElementById("loginForm");
  let selectedRole = "patient";

  roleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      roleButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
      selectedRole = button.dataset.role;
    });
  });

  // Login form submission
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Simple validation
    if (!username || !password) {
      alert("Please fill in all fields");
      return;
    }

    try {
      // Here you would normally make an API call
      // For demo, we'll redirect based on role
      switch (selectedRole) {
        case "admin":
          window.location.href = "admin-dashboard.html";
          break;
        case "doctor":
          window.location.href = "doctor-dashboard.html";
          break;
        case "patient":
          window.location.href = "patient-dashboard.html";
          break;
      }
    } catch (error) {
      alert("Login failed. Please try again.");
    }
  });
});
