document.addEventListener("DOMContentLoaded", function () {
  const doctors = [
    {
      id: 1,
      name: "Dr. John Smith",
      department: "Cardiology",
      experience: "15 years",
      availability: "Mon-Fri",
    },
    {
      id: 2,
      name: "Dr. Sarah Johnson",
      department: "Neurology",
      experience: "12 years",
      availability: "Mon-Wed",
    },
    {
      id: 3,
      name: "Dr. Michael Brown",
      department: "Orthopedics",
      experience: "10 years",
      availability: "Tue-Sat",
    },
  ];

  const doctorsGrid = document.querySelector(".doctors-grid");
  const departmentFilter = document.getElementById("departmentFilter");
  const searchDoctor = document.getElementById("searchDoctor");

  function createDoctorCard(doctor) {
    return `
            <div class="doctor-card">
                <div class="doctor-image">${doctor.name[3]}</div>
                <div class="doctor-info">
                    <h3 class="doctor-name">${doctor.name}</h3>
                    <p class="doctor-dept">${doctor.department}</p>
                    <div class="doctor-details">
                        <p>Experience: ${doctor.experience}</p>
                        <p>Available: ${doctor.availability}</p>
                    </div>
                    <div class="doctor-actions">
                        <button class="btn-primary" onclick="bookAppointment(${doctor.id})">Book Appointment</button>
                        <button class="btn-secondary" onclick="viewProfile(${doctor.id})">View Profile</button>
                    </div>
                </div>
            </div>
        `;
  }

  function renderDoctors(doctorsList) {
    doctorsGrid.innerHTML = doctorsList
      .map((doctor) => createDoctorCard(doctor))
      .join("");
  }

  function filterDoctors() {
    const department = departmentFilter.value.toLowerCase();
    const searchTerm = searchDoctor.value.toLowerCase();

    const filtered = doctors.filter((doctor) => {
      const matchesDepartment =
        !department || doctor.department.toLowerCase() === department;
      const matchesSearch =
        doctor.name.toLowerCase().includes(searchTerm) ||
        doctor.department.toLowerCase().includes(searchTerm);
      return matchesDepartment && matchesSearch;
    });

    renderDoctors(filtered);
  }

  departmentFilter.addEventListener("change", filterDoctors);
  searchDoctor.addEventListener("input", filterDoctors);

  // Initial render
  renderDoctors(doctors);
});

function bookAppointment(doctorId) {
  // Implement appointment booking logic
  console.log("Booking appointment with doctor:", doctorId);
}

function viewProfile(doctorId) {
  // Implement profile viewing logic
  console.log("Viewing profile of doctor:", doctorId);
}
