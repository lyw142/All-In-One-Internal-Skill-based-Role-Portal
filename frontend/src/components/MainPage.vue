<template>
  <div>
    <div class="navbar">
      <div class="navbar-left">
        <img src="logo.png" alt="Logo" class="logo" />
        <a to="/roles" class="nav-link">Roles</a>
        <a to="/candidates" class="nav-link">Candidates</a>
        <a to="/view-staff-skills" class="nav-link">View Staff Skills</a>
      </div>
      <div class="navbar-right">
        <button class="btn btn-secondary">Logout</button>
      </div>
    </div>
    <div class="row mb-3" :style="{ padding: '10px 20px' }">
      <div class="col-md-6" :style="{ textAlign: 'left' }">
        <span>Roles </span>
        <button
          :class="{
            'btn-secondary': selectedStatus === 'open',
            'btn-outline-secondary': selectedStatus !== 'open',
          }"
          class="btn btn-sm btn pr-2"
          @click="toggleStatus('open')"
        >
          Open and paused ({{ openCount }})
        </button>
        <button
          :class="{
            'btn-secondary': selectedStatus === 'closed',
            'btn-outline-secondary': selectedStatus !== 'closed',
          }"
          class="btn btn-sm btn"
          @click="toggleStatus('closed')"
        >
          Closed ({{ closedCount }})
        </button>
      </div>
      <div class="col-md-6" :style="{ textAlign: 'right' }">
        <button class="btn btn-secondary" @click="createRole">
          Create Role
        </button>
      </div>
    </div>
    <div class="container mt-4">
      <div class="row mb-4">
        <div class="col-md-8">
          <input
            type="text"
            class="form-control"
            placeholder="Search for a role..."
            v-model="searchQuery"
          />
        </div>
      </div>
      <div :style="{ display: 'flex' }">
        <div :style="{ width: '40%' }">
          <div
            v-for="(role, index) in roles"
            :key="index"
            @click="roleClicked(role.listingID)"
          >
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">{{ role.title }}</h5>
                <p class="card-text">
                  <strong>Skills Required:</strong>
                  <span
                    v-for="(skill, index) in role.skills.split(',')"
                    :key="index"
                    class="skill-box"
                  >
                    {{ skill.trim() }}
                  </span>
                </p>
                <ul>
                  <li
                    v-for="(line, index) in role.description.split('\n')"
                    :key="index"
                  >
                    {{ line }}
                  </li>
                </ul>
                <p class="card-text">
                  <strong>Application Deadline:</strong> Closed in
                  {{ role.deadline }} days
                </p>
              </div>
            </div>
          </div>
          <div v-if="roles.length===0">
          <h3>
          There are no listings available at the moment
          </h3>
          </div>
        </div>
        <div :style="{ width: '60%', marginLeft: '16px' }">
          <div class="card" v-if="selectedRole">
            <div>
              <div class="divider">
                <h3 class="card-title">{{ selectedRole.Role_Name }}</h3>
                <p>{{ selectedRole.Salary }}</p>
                <button class="btn btn-secondary" @click="editRole()">
                  Edit role
                </button>
              </div>
              <div class="divider">
                <h3 class="card-title">Role description</h3>
                <div class="role-description">
                  <strong>Job responsabilities</strong>
                  <ol>
                    <li>
                      {{ selectedRole.Role_Responsibilities }}
                    </li>
                  </ol>
                </div>

                <!-- Role Requirements -->
                <div class="role-requirements">
                  <strong>Role Requirements</strong>
                  <ol>
                    <li>
                      {{ selectedRole.Role_Requirements }}
                    </li>
                  </ol>
                </div>
              </div>
              <div class="skills">
                <p>
                  <strong>Skills Required:</strong>
                </p>
                <span
                  v-for="(skill, index) in selectedRole.Skills"
                  :key="index"
                  class="skill-box"
                >
                  {{ skill.trim() }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // Import Axios library

export default {
  data() {
    return {
      openCount: 1,
      closedCount: 0,
      searchQuery: "",
      editOpen: false,
      jobListings: [], // New property to store job listings
      selectedStatus: "open", // Default selected status
      roles: [
        {
          title: "Human Resource (Entry Level)",
          skills: "Communication, Recruitment, HR Policies",
          description:
            "We are seeking an Entry Level Human Resource professional to join our team. This role involves assisting with recruitment, onboarding, and HR policy compliance.\n Ideal candidates should have strong communication skills and a desire to grow in the field of HR.",
          deadline: 7, // Number of days until the application deadline
        },
        {
          title: "Human Resource Officer",
          skills: "Employee Relations, Benefits Administration, HR Compliance",
          description:
            "We are looking for an experienced Human Resource Officer to manage HR functions, including employee relations, benefits administration, and ensuring HR compliance.\n The ideal candidate should have a strong background in HR and excellent problem-solving skills.",
          deadline: 14, // Number of days until the application deadline
        },
        {
          title: "Real Estate Sale Coordinator",
          skills: "Real Estate Sales, Customer Service, Negotiation",
          description:
            "Join our real estate team as a Sale Coordinator!\n This role involves coordinating real estate transactions, providing excellent customer service to clients, and assisting with negotiations.\n If you have a passion for real estate and a customer-centric approach, we want to hear from you.",
          deadline: 5, // Number of days until the application deadline
        },
        // Add more role objects as needed
      ],
      selectedRole: null,
    };
  },
  methods: {
    toggleStatus(status) {
      // Implement your logic to toggle between open and closed roles
      // Update openCount and closedCount accordingly
      this.selectedStatus = status;
      this.selectedRole = null;
      this.loadJobListings();
    },
    createRole() {
      // Implement your logic to create a new role
    },

    calculateDeadline(deadline) {
      const today = new Date();
      const deadlineDate = new Date(deadline);
      const timeDifference = deadlineDate - today;
      const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
      return daysRemaining;
    },
    loadJobListings() {
      const apiUrl = `http://127.0.0.1:5000/api/${
        this.selectedStatus === "open" ? "open" : "closed"
      }joblistings`;

      axios
        .get(apiUrl)
        .then((response) => {
          // Update jobListings with the API response data
          this.jobListings = response.data;
          this.roles = response.data.map((listing) => ({
            listingID: listing.Listing_ID,
            title: listing.Role_Name,
            skills: listing.Skills.join(", "),
            description: listing.Role_Responsibilities,
            deadline: this.calculateDeadline(listing.Deadline), // Calculate the remaining days
          }));
        })
        .catch((error) => {
          console.error("Error fetching job listings:", error);
        });
    },
    fetchRoleDetails(listingID) {
      const apiUrl = `http://127.0.0.1:5000/api/getRoleListing/${listingID}`;

      axios
        .get(apiUrl)
        .then((response) => {
          const data = response.data[0];
          // Set selectedRole to the API response data
          this.selectedRole = { ...data };
        })
        .catch((error) => {
          console.error("Error fetching role details:", error);
        });
    },
    roleClicked(listingID) {
      // Call the fetchRoleDetails method

      this.fetchRoleDetails(listingID);
    },
    editRole() {
      // Use a prompt dialog to collect user input for editing
      const newJobRequirements = prompt(
        "Enter requirements for the role:",
        this.selectedRole.Role_Requirements
      );
      // Update the role title if the user provided a value
      if (newJobRequirements !== null) {
        this.selectedRole.Role_Requirements = newJobRequirements;
        axios
          .post(
            `http://127.0.0.1:5000/api/updateRoleListing/${this.selectedRole.Listing_ID}`,
            this.selectedRole
          )
          .then((response) => {
            console.log({ response });
          });
      }
    },
  },
  mounted() {
    // Load job listings when the component is mounted
    this.loadJobListings();
  },
};
</script>

<style scoped>
/* Existing navbar styles */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #333;
  padding: 10px 20px;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 40px;
  height: 40px;
  margin-right: 20px;
}

.nav-link {
  text-decoration: none;
  margin-right: 20px;
  color: #333;
  font-size: 16px;
}

.nav-link:last-child {
  margin-right: 0;
}

/* New content styles */
.container {
  margin-top: 20px;
}

.btn-success {
  background-color: #28a745;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-primary {
  background-color: #007bff;
}

/* Adjust button text color */
.btn-success,
.btn-secondary,
.btn-primary {
  color: #fff;
}

/* Style the search input */
.form-control {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.card-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}
.card,
.card-body {
  text-align: left;
}
.card-text {
  font-size: 16px;
  margin-bottom: 10px;
}
.skill-box {
  display: inline-block;
  background-color: rgba(25, 135, 84, 0.1);
  padding: 4px 8px;
  margin-right: 5px;
  margin-bottom: 5px;
  border-radius: 4px;
  font-size: 14px;
}
.divider {
  padding: 12px 36px;
  border-bottom: 1px solid rgba(25, 135, 84, 0.1);
}
.skills {
  padding: 12px 36px;
}
</style>
