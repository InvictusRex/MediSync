document.addEventListener("DOMContentLoaded", function () {
  const appointmentForm = document.getElementById("appointmentForm");
  const departmentSelect = document.getElementById("department");
  const doctorSelect = document.getElementById("doctor");
  const dateInput = document.getElementById("appointmentDate");
  const timeSelect = document.getElementById("appointmentTime");

  // Mock data for doctors
  const doctors = {
    cardiology: ["Dr. John Smith", "Dr. Sarah Johnson"],
    neurology: ["Dr. Michael Brown", "Dr. Emily Davis"],
    orthopedics: ["Dr. Robert Wilson", "Dr. Lisa Anderson"],
  };

  // Mock data for available time slots
  const timeSlots = [
    "09:00 AM",
    "09:30 AM",
    "10:00 AM",
    "10:30 AM",
    "11:00 AM",
    "11:30 AM",
    "02:00 PM",
    "02:30 PM",
    "03:00 PM",
    "03:30 PM",
    "04:00 PM",
    "04:30 PM",
  ];

  // Set minimum date to today
  const today = new Date().toISOString().split("T")[0];
  dateInput.min = today;

  // Update doctors when department changes
  departmentSelect.addEventListener("change", function () {
    const department = this.value;
    doctorSelect.innerHTML = '<option value="">Select Doctor</option>';

    if (department && doctors[department]) {
      doctors[department].forEach((doctor) => {
        const option = document.createElement("option");
        option.value = doctor;
        option.textContent = doctor;
        doctorSelect.appendChild(option);
      });
    }
  });

  // Update time slots when date changes
  dateInput.addEventListener("change", function () {
    timeSelect.innerHTML = '<option value="">Select Time</option>';

    timeSlots.forEach((time) => {
      const option = document.createElement("option");
      option.value = time;
      option.textContent = time;
      timeSelect.appendChild(option);
    });
  });

  // Handle form submission
  appointmentForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = {
      department: departmentSelect.value,
      doctor: doctorSelect.value,
      date: dateInput.value,
      time: timeSelect.value,
      reason: document.getElementById("reason").value,
    };

    console.log("Booking appointment:", formData);
    alert("Appointment booked successfully!");

    // Close modal and reset form
    const modal = this.closest(".modal");
    modal.classList.remove("active");
    this.reset();
  });
});
