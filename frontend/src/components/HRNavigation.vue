<template>
  <div>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
      <div class="navbar-left">
        <img src="../assets/logo.png" alt="Logo" class="logo" />
        <a href="/roles" class="nav-link" style="color: white;">View roles</a>
        <a href="/candidates" class="nav-link" style="color: white;">Candidates</a>
        <a href="/view-staff-skills" class="nav-link" style="color: white;">View Staff Skills</a>
      </div>
      <div class="navbar-right">
        <button class="btn btn-secondary" @click="clearUserSessionData()">Logout</button>
      </div>
    </div>
    <div class="row mb-3" :style="{ padding: '10px 20px' }">
      <div class="col-md-6" :style="{ textAlign: 'left' }">
        <span>Roles </span>
        <button :class="{
          'btn-secondary': selectedStatus === 'open',
          'btn-outline-secondary': selectedStatus !== 'open',
        }" class="btn btn-sm btn pr-2" @click="toggleStatus('open')">
          Open and paused <span v-if="openCount !== null">({{ openCount }})</span>
        </button>
        <button :class="{
          'btn-secondary': selectedStatus === 'closed',
          'btn-outline-secondary': selectedStatus !== 'closed',
        }" class="btn btn-sm btn" @click="toggleStatus('closed')">
          Closed <span v-if="closedCount !== null">({{ closedCount }})</span>
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
          <input type="text" class="form-control" placeholder="Search for a role..." v-model="searchQuery" />
        </div>
      </div>
      <div :style="{ display: 'flex' }">
        <div :style="{ width: '40%' }">
          <div v-for="(role, index) in roles" :key="index"
            @click="roleClicked(role.listingID), selectRole(role), countMatchingSkills(), updateProgressBar()">
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">{{ role.title }}</h5>
                <p class="card-text">
                  <strong>Skills Required:</strong>
                  <span v-for="skill in role.skills.split(',')" class="skill-box" :style="{
                    backgroundColor: userSkills.includes(skill.trim()) ? 'rgba(25, 135, 84, 0.8)' : 'rgba(25, 135, 84, 0.1)',
                    color: userSkills.includes(skill.trim()) ? 'white' : 'inherit'
                  }"> {{ skill.trim() }}
                  </span>
                </p>
                <ul>
                  <li v-for="(line, index) in role.description.split('\n')" :key="index">
                    {{ line }}
                  </li>
                </ul>
                <p class="card-text">
                  <strong>Application Deadline:</strong> {{ (role.deadline) <= 0 ? 'Closed' : (role.deadline) + ' (' +
                    this.calculateDeadline(role.deadline) + ' days remaining)' }} </p>
                    <p class="card-text">
                      <strong>Application Date Posted:</strong>
                      {{ role.dateposted }}
                    </p>
              </div>
            </div>
          </div>
          <div v-if="roles.length === 0">
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
                <p>${{ (selectedRole.Salary / 12).toFixed(0) }} per month, Full time</p>
                <button class="btn btn-secondary" @click="editRole()">
                  Edit role
                </button>
              </div>
              <div class="divider">
                <h3 class="card-title">Role description</h3>
                <div class="role-description">
                  <strong>Job responsibilities</strong>
                  <p>
                    {{ selectedRole.Role_Responsibilities }}
                  </p>
                </div>

                <!-- Confirmation modal (initially hidden) -->
                <div class="modal-container" v-if="showConfirmModal">
                  <div class="confirmation-modal">
                    <p>Are you sure you want to submit an application for the role of {{ selectedRole.Role_Name }}?</p>
                    <button class="btn btn-primary" style="width: 120px; height: 40px; margin-right: 10px;"
                      @click="submitApplication">Confirm</button>
                    <button class="btn btn-secondary" style="width: 120px; height: 40px; margin-left: 10px;"
                      @click="cancelApplication">Cancel</button>
                  </div>
                </div>
                <!-- Success Modal -->
                <div class="modal-container" v-if="showSuccessModal">
                  <div class="confirmation-modal">
                    <p>Your application has been successfully submitted.</p>
                    <button class="btn btn-primary" @click="returnToJobListings">Return to job listings</button>
                  </div>
                </div>
                <!-- Role Requirements -->
                <div class="role-requirements">
                  <strong>Role Requirements</strong>
                  <ol>
                    <li v-for="(requirement, index) in selectedRole.Role_Requirements" :key="index">
                      {{ requirement }}
                    </li>
                  </ol>
                </div>
              </div>
              <div class="skills">
                <p>
                  <strong>How you match</strong>
                </p>
                <div class="progress " role="progressbar" aria-label="Basic example" aria-valuenow="0" aria-valuemin="0"
                  aria-valuemax="100" style="margin-bottom: 10px;">
                  <div class="progress-bar bg-success" :style="{ width: progressBarWidth }">{{ progressBarWidth }}</div>
                </div>
                <p>{{ this.matching_skills.length }} skill(s) on your profile, {{ this.skill_list.length -
                  this.matching_skills.length }} skill(s) missing from your profile</p>
                <span v-for="skill in selectedRole.Skills" class="skill-box" :style="{
                  backgroundColor: userSkills.includes(skill.trim()) ? 'rgba(25, 135, 84, 0.8)' : 'rgba(25, 135, 84, 0.1)',
                  color: userSkills.includes(skill.trim()) ? 'white' : 'inherit'
                }">
                  {{ skill.trim() }}
                </span>
              </div>

              <div>
                <button class="btn btn-secondary" style="margin: 10px;" @click="showConfirmationModal(selectedRole)"
                  :disabled="hasAppliedForRole">
                  {{ hasAppliedForRole ? 'Applied' : 'Apply for role' }}
                </button>
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
import Cookies from 'js-cookie'

export default {
  data() {
    return {
      openCount: null,
      closedCount: null,
      searchQuery: "",
      editOpen: false,
      jobListings: [], // New property to store job listings
      selectedStatus: "open", // Default selected status
      roles: [],
      userSkills: [],
      skill_list: [],
      matching_skills: [],
      progressBarWidth: "",
      selectedRole: null,
      staff_id: null,
      showConfirmModal: false, // Initially hidden
      showSuccessModal: false, // Add a new property to control the success modal
      hasAppliedForRole: false, // Define the hasAppliedForRole property
      applicationProcessing: false, // Add a property to track application processing
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
      this.$router.push({ name: "CreateRoleListing" });
    },

    calculateDeadline(deadline) {
      const today = new Date();
      const deadlineDate = new Date(deadline);
      const timeDifference = deadlineDate - today;
      const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
      return daysRemaining;
    },
    loadJobListings() {
      const apiUrl = `http://127.0.0.1:5000/api/${this.selectedStatus === "open" ? "open" : "closed"
        }joblistings`;

      axios
        .get(apiUrl)
        .then((response) => {
          // Update jobListings with the API response data
          this.jobListings = response.data;
          if (this.selectedStatus === "open") { this.openCount = this.jobListings.length; }
          else { this.closedCount = this.jobListings.length; }
          this.roles = response.data.map((listing) => ({
            listingID: listing.Listing_ID,
            title: listing.Role_Name,
            skills: listing.Skills.join(", "),
            description: listing.Role_Responsibilities,
            deadline: listing.Deadline, // Calculate the remaining days
            dateposted: listing.Date_Posted,
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
      const Listing_ID = this.selectedRole.Listing_ID;
      this.$router.push({ name: "UpdateRoleListing", params: { Listing_ID } });
      // if (newJobRequirements !== null) {
      //   this.selectedRole.Role_Requirements = newJobRequirements;
      //   axios
      //     .post(
      //       `http://127.0.0.1:5000/api/updateRoleListing/${this.selectedRole.Listing_ID}`,
      //       this.selectedRole
      //     )
      //     .then((response) => {
      //       console.log({ response });
      //     });
      // }
    },
    // Retrieve user session data from a cookie
    getUserSessionData() {
      const serializedUser = Cookies.get('userSession')
      if (serializedUser) {
        const data = JSON.parse(serializedUser);
        this.staff_id = data.Staff_ID;
        if (!(data.Access_Rights == 4)) {
          this.$router.push("/staffnav");
        }
      } else {
        this.$router.push("/");; // No user session data found
      }
    },
    getUserSkills() {
      axios.get('http://127.0.0.1:5000/api/getStaffSkills/' + this.staff_id)
        .then(response => {
          response.data.forEach(skill => {
            // Append the skill_name to the userSkills array
            this.userSkills.push(skill.Skill_Name);
          });
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    countMatchingSkills() {
      this.skill_list = this.selectedRole.skills.split(',');
      this.matching_skills = this.skill_list.filter(skill => this.userSkills.includes(skill));

    },
    updateProgressBar() {
      const pctbar = Math.round((this.matching_skills.length / this.skill_list.length) * 100).toString();
      this.progressBarWidth = pctbar + "%";
    },
    // Clear user session data from the cookie
    clearUserSessionData() {
      Cookies.remove('userSession');
      this.$router.push("/");; // No user session data found
    },
    showConfirmationModal(role) {
      console.log('Clicked role:', role);
      this.showConfirmModal = true;
    },

    returnToJobListings() {
      this.showSuccessModal = false;
    },

    submitApplication() {
      console.log('Submitting application for the role: ', this.selectedRole.Role_Name);

      // Set the applicationProcessing to true to indicate processing
      this.applicationProcessing = true;

      // Prepare the data for the API request
      const data = {
        Listing_ID: this.selectedRole.Listing_ID,
        Staff_ID: this.staff_id,
      };

      // Send the API request to apply for the role
      axios.post('http://127.0.0.1:5000/api/applyforopenrole', data)
        .then(response => {
          // Application was successfully created

          // Update the button state to "Applied" immediately
          this.hasAppliedForRole = true;

          // Show the success modal
          this.showSuccessModal = true;
        })
        .catch(error => {
          console.error('Error submitting application:', error);

          // Handle the error or show an error message to the user
        })
        .finally(() => {
          // Set applicationProcessing to false to indicate processing has finished
          this.applicationProcessing = false;

          // Close the confirmation modal
          this.showConfirmModal = false;
        });
    },

    cancelApplication() {
      // Cancel the application and hide the confirmation modal
      this.showConfirmModal = false;
    },
    async selectRole(role) {
      // Set the selected role
      this.selectedRole = role;
      this.isCardClicked = true;
      // Check if the user has already applied for this role
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/checkApplicationStatus/${this.staff_id}/${role.listingID}`
        );

        // Check the response to determine if the user has applied
        this.hasAppliedForRole = response.data.hasApplied; // Adjust the response structure as needed
      } catch (error) {
        console.error('Error checking application status:', error);
      }
    },

  },
  mounted() {
    this.getUserSessionData();
    this.getUserSkills();
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

.confirmation-modal {
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  /* Semi-transparent background to darken the content */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  /* Make sure the modal is above other elements */
}


.btn-primary {
  background-color: rgba(25, 135, 84, 0.1);
  /* Updated to green color */
  color: #000;
  /* Black text */
  border: none;
}

/* Add hover animation for the "Show Results" button */
.btn-primary:hover {
  background-color: rgba(25, 135, 84, 0.8);
  /* Darker shade of green */
  color: #fff;
  /* Font color */
}
</style>
