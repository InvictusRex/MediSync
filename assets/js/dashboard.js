document.addEventListener("DOMContentLoaded", function () {
  // Modal handling
  const modals = document.querySelectorAll(".modal");
  const modalTriggers = document.querySelectorAll("[data-modal]");
  const closeModalButtons = document.querySelectorAll(".close-modal");

  // Open modal
  modalTriggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const modalId = trigger.dataset.modal;
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.classList.add("active");
      }
    });
  });

  // Close modal
  const closeModal = (modal) => {
    modal.classList.remove("active");
  };

  closeModalButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const modal = button.closest(".modal");
      closeModal(modal);
    });
  });

  // Close modal when clicking outside
  modals.forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
  });

  // Add Doctor form handling
  const addDoctorForm = document.getElementById("addDoctorForm");
  if (addDoctorForm) {
    addDoctorForm.addEventListener("submit", (e) => {
      e.preventDefault();
      // Add doctor logic here
      const formData = new FormData(addDoctorForm);
      console.log("Adding doctor:", Object.fromEntries(formData));
      // Close modal after submission
      const modal = addDoctorForm.closest(".modal");
      closeModal(modal);
      addDoctorForm.reset();
    });
  }

  // Add Doctor button
  const addDoctorBtn = document.getElementById("addDoctorBtn");
  if (addDoctorBtn) {
    addDoctorBtn.addEventListener("click", () => {
      const modal = document.getElementById("addDoctorModal");
      if (modal) {
        modal.classList.add("active");
      }
    });
  }

  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector(".mobile-menu-toggle");
  const sidebar = document.querySelector(".sidebar");

  if (mobileMenuToggle && sidebar) {
    mobileMenuToggle.addEventListener("click", () => {
      sidebar.classList.toggle("active");
    });
  }

  // Table row actions
  const actionButtons = document.querySelectorAll(".data-table button");
  actionButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      const action = e.target.textContent.toLowerCase();
      const row = e.target.closest("tr");
      const name = row.cells[0].textContent;

      if (action === "remove") {
        if (confirm(`Are you sure you want to remove ${name}?`)) {
          row.remove();
        }
      } else if (action === "edit") {
        // Implement edit functionality
        console.log("Editing:", name);
      }
    });
  });
});
