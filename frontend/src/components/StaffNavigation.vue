<template>
  <div>
    <!-- Navbar -->
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
      <div class="navbar-left">
        <img src="../assets/logo.png" alt="Logo" class="logo" />
        <a to="/roles" class="nav-link" style="color: white;">View roles</a>
      </div>
      <div class="navbar-right">
        <button class="btn btn-secondary" @click="clearUserSessionData()">Logout</button>
      </div>
    </div>
    <!-- Main content -->
    <div class="container mt-4">
      <!-- Search and Filter bar -->
      <div class="row mb-4">
        <div class="col-md-10">
          <input type="text" class="form-control" placeholder="Search for a role..." v-model="searchQuery" />
        </div>

        <!-- Filter dropdown for skills selection -->
        <div class="col-md-2">
          <div class="dropdown">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="skillsDropdown" data-bs-toggle="dropdown"
              aria-haspopup="true" aria-expanded="false">
              Filter by Skills
            </button>
            <div class="dropdown-menu" aria-labelledby="skillsDropdown" @click.stop>
              <!-- Checklist of skills with checkboxes -->
              <div v-for="skill in skills" :key="skill.Skill_ID">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="selectedSkills" :value="skill" class="checkbox-input" />
                  <span class="checkbox-text">{{ skill.Skill_Name }}</span>
                </label>
              </div>
              <!-- Action buttons -->
              <!-- Action buttons -->
              <button class="dismiss-button" @click.stop="cancelFilter">×</button>


              <div class="filter-buttons">
                <button class="btn btn-secondary" @click="clearFilter">Clear Filter</button>
                <button class="btn btn-primary" @click="applyFilter">Show Results</button>
              </div>
              <!-- Display a message when no skills are selected -->
              <div class="filter-message" v-if="showNoSkillsMessage">
                {{ showNoSkillsMessage }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Role listings -->
      <div :style="{ display: 'flex' }" v-if="roles.length > 0">
        <div :style="{ width: '40%' }">
          <div v-for="role in roles" @click="selectRole(role), countMatchingSkills(role), updateProgressBar()">
            <div :class="{ 'card': true, 'green-border': role === selectedRole, 'mb-3': true }">
              <div class="card-body">
                <h5 class="card-title">{{ role.Role_Name }}</h5>
                <p class="card-text">
                  <strong>Skills Required:</strong>
                  <span v-for="skill in role.Skills" class="skill-box" :style="{
                    backgroundColor: userSkills.includes(skill.trim()) ? 'rgba(25, 135, 84, 0.8)' : 'rgba(25, 135, 84, 0.1)',
                    color: userSkills.includes(skill.trim()) ? 'white' : 'inherit'
                  }">
                    {{ skill.trim() }}
                  </span>
                </p>
                <p class="card-text">
                  <strong>Application Deadline:</strong>
                  {{ role.Deadline }}, {{ this.calculateDeadline(role.Deadline) }} day(s) remaining

                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Role details -->
        <div :style="{ width: '60%', marginLeft: '16px' }">
          <div class="card overflow-y-auto" v-if="isCardClicked" id="roledescription">
            <div>
              <div class="divider">
                <h3 class="card-title">{{ selectedRole.Role_Name }}</h3>
                <p>${{ selectedRole.Salary }} a month, Full time</p>
              </div>
              <div class="divider">
                <h3 class="card-title">Role description</h3>
                <div class="role-description">
                  <strong>Job responsibilities</strong>
                  <div style="margin-bottom: 20px;margin-top: 5px;">
                    {{ selectedRole.Role_Responsibilities }}

                  </div>
                </div>

              <!-- Confirmation modal (initially hidden) -->
              <div class="modal-container" v-if="showConfirmModal">
                <div class="confirmation-modal">
                  <p>Are you sure you want to submit an application for the role of {{ selectedRole.Role_Name }}?</p>
                  <button class="btn btn-primary" style="width: 120px; height: 40px; margin-right: 10px;" @click="submitApplication">Confirm</button>
                  <button class="btn btn-secondary" style="width: 120px; height: 40px; margin-left: 10px;" @click="cancelApplication">Cancel</button>
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
                  <ul style="margin-top: 5px;">
                    <li v-for="line in selectedRole.Role_Requirements">
                      {{ line }}
                    </li>
                  </ul>
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
                <p>{{ countMatchingSkills(selectedRole) }} skill(s) on your profile, {{ selectedRole.Skills.length -
                  countMatchingSkills(selectedRole) }} skill(s) missing from your profile</p>
                <span v-for="skill in selectedRole.Skills" class="skill-box" :style="{
                  backgroundColor: userSkills.includes(skill.trim()) ? 'rgba(25, 135, 84, 0.8)' : 'rgba(25, 135, 84, 0.1)',
                  color: userSkills.includes(skill.trim()) ? 'white' : 'inherit'
                }">
                  {{ skill.trim() }}
                </span>
              </div>
              <div>
                <button
  class="btn btn-secondary"
  style="margin: 10px;"
  @click="showConfirmationModal(selectedRole)"
  :disabled="hasAppliedForRole"
>
  {{ hasAppliedForRole ? 'Applied' : 'Apply for role' }}
</button>

              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No available roles message -->
      <div v-if="roles.length == 0">
        There are no available roles at the moment
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'

export default {
  data() {
    return {
      searchQuery: "",
      roles: [],
      selectedRole: {},
      isCardClicked: false,
      isActive: false,
      userSkills: [],
      skills: [], // Add this property to store skills
      selectedSkills: [], // Add this property to store selected skills
      progressBarWidth: "",
      showNoSkillsMessage: false, // Add this property to track the message display
      isDropdownOpen: false, // Add this property to track the dropdown state
      staff_id: null,
      selectedRole: null, // Role selected for application
      showConfirmModal: false, // Initially hidden
      showSuccessModal: false, // Add a new property to control the success modal
      hasAppliedForRole: false, // Define the hasAppliedForRole property
    };
  },
  methods: {
    // Your methods...
    showConfirmationModal(role) {
        console.log('Clicked role:', role);
        this.showConfirmModal = true;
    },

    returnToJobListings() {
        this.showSuccessModal = false;
    },

    submitApplication() {
      console.log('Submitting application for the role: ', this.selectedRole.Role_Name);

      // Check the Staff_ID and Listing_ID before making the request
      console.log('Staff_ID:', this.staff_id); // Replace with the actual Staff ID
      console.log('Listing_ID:', this.selectedRole.Listing_ID);

      // Define the data to be sent in the request (for testing purposes)
      const data = {
          Listing_ID: this.selectedRole.Listing_ID,
          Staff_ID: this.staff_id,
        };

      console.log('Data being sent for testing:', data);

      // For testing, you can log the data and skip the API request
      // console.log('Testing: Application data would be sent but not actually submitted to the API.');
      this.showConfirmModal = false;
      console.log('Testing: Confirmation modal should be closed');

      // This part would be replaced with an actual API request in the production version
      axios.post('http://127.0.0.1:5000/api/applyforopenrole', data)
        .then(response => {
          // Application was successfully created
          console.log('Application submitted successfully:', response.data.message);
          // You can perform additional actions here if needed
           })
           .catch(error => {
             console.error('Error submitting application:', error);
             // Handle the error or show an error message to the user
           })
           .finally(() => {
             // Close the confirmation modal, regardless of success or failure
             this.showConfirmModal = false;
           });

        // Assuming a successful API request
        // You would typically make the API request and handle the response
        // For this demonstration, we'll directly show the success modal
      this.showSuccessModal = true;

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
      `http://127.0.0.1:5000/api/checkApplicationStatus/${this.staff_id}/${role.Listing_ID}`
    );

    // Check the response to determine if the user has applied
    this.hasAppliedForRole = response.data.hasApplied; // Adjust the response structure as needed
  } catch (error) {
    console.error('Error checking application status:', error);
  }},

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

    calculateDeadline(deadline) {
      const today = new Date();
      const deadlineDate = new Date(deadline);
      const timeDifference = deadlineDate - today;
      const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
      return daysRemaining;
    },
    toggleActive() {
      this.isActive = !this.isActive;
    },
    countMatchingSkills(role) {
      // Filter the role.Skills array to include only skills that are in userSkills
      const matchingSkills = role.Skills.filter(skill => this.userSkills.includes(skill.trim()));
      // Return the count of matching skills
      return matchingSkills.length;
    },
    updateProgressBar() {
      const pctbar = ((this.countMatchingSkills(this.selectedRole) / this.selectedRole.Skills.length) * 100).toString();
      this.progressBarWidth = pctbar + "%";
    },
    // Function to fetch skills from the API
    fetchSkills() {
      axios.get('http://127.0.0.1:5000/api/skills').then(response => { this.skills = response.data; }).catch(error => {
        console.error('Error fetching skills:', error);
      });
    },

    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },

    cancelFilter() {
      this.isDropdownOpen = false; // Close the filter dropdown
    },

    clearFilter() {
      // Check if no skills were previously selected (no filter applied)
      if (this.selectedSkills.length === 0) {
        // Display a message indicating that no filter is applied
        this.showNoSkillsMessage = 'No filter is currently applied.';
      } else {
        // Reset the message and uncheck all selected skills
        this.showNoSkillsMessage = false;
        this.selectedSkills = [];

        // Reset the job listings to their pre-filter state
        this.fetchAllRoles();
      }
    },

    async fetchAllRoles() {
      try {
        // Make an API request to fetch all roles without any filter
        const response = await axios.get('http://127.0.0.1:5000/api/openjoblistings');

        // Update the roles data property with all roles
        this.roles = response.data;
      } catch (error) {
        console.error('Error fetching all roles:', error);
      }
    },
    async applyFilter() { // Declare applyFilter as an async function
      // Check if no skills are selected
      if (this.selectedSkills.length === 0) {
        // Display a message indicating that at least one skill should be selected
        this.showNoSkillsMessage = 'Please select at least one skill.';
      } else {
        // If skills are selected, reset the message and proceed with filtering
        this.showNoSkillsMessage = false;

        // Assuming you have an array of selected skill IDs in this.selectedSkills
        const selectedSkillIds = this.selectedSkills.map(skill => skill.Skill_ID);

        // Log the selected skill IDs to the console for debugging
        console.log('Selected Skill IDs:', selectedSkillIds);
        console.log('API Request input:', selectedSkillIds.join(","))

        try {
          // Make an API request to filter role listings based on selected skills
          const response = await axios.get(`http://127.0.0.1:5000/api/filterRoleListingBySkill/${selectedSkillIds.join(",")}`);

          // Update the roles data property with the filtered role listings
          this.roles = response.data;
        } catch (error) {
          console.error('Error filtering role listings:', error);
        }
      }
    },

    // Retrieve user session data from a cookie
    getUserSessionData() {
      const serializedUser = Cookies.get('userSession');
      if (serializedUser) {
        const userData = JSON.parse(serializedUser);
        this.staff_id = userData.Staff_ID;
      } else {
        this.$router.push("/");; // No user session data found
      }
    },

    // Clear user session data from the cookie
    clearUserSessionData() {
      Cookies.remove('userSession');
      this.$router.push("/");; // No user session data found
    }
  },
  mounted() {
    // Call the method to fetch skills when the component is mounted
    this.getUserSessionData();
    this.fetchSkills();
    this.getUserSkills();

    axios.get('http://127.0.0.1:5000/api/openjoblistings')
      .then(response => {
        this.roles = response.data;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
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

/* Buttons */
.btn-success {
  background-color: #28a745;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-primary {
  background-color: rgba(25, 135, 84, 0.1);
  /* Start with green color */
  color: #000;
  /* Black text */
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

/* Adjust button text color */
.btn-primary:hover {
  background-color: rgba(25, 135, 84, 0.8);
  /* Darker green on hover */
  color: #fff;
  /* White text on hover */
}

/* Style the search input */
.form-control {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Card styles */
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

/* Dropdown styles */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-toggle {
  background-color: rgba(25, 135, 84, 0.1);
  /* Updated to green color */
  color: #333;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  display: none;
  width: 300px;
  /* Increased width for more space */
  background-color: #fff;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  padding: 10px;
  /* Added padding to the modal */
}

.dropdown-menu.show {
  display: block;
}

.dismiss-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  position: absolute;
  top: 10px;
  right: 10px;
  color: #333;
  /* Reverted to grey */
}

/* Swap the positions of "Show Results" and "Clear Filter" buttons */
.filter-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  /* Added margin to separate buttons from checkboxes */
  order: 1;
  /* Swap the order */
}

/* Remove the blue outline from the "Show Results" button */
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

/* Revert to original checkbox styles */
.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 0;
  /* Added padding between checkbox items */
}

.checkbox-label input[type="checkbox"] {
  margin-right: 10px;
}

.green-border {
  border-color: rgba(25, 135, 84, 0.8);
  /* Darker shade of green */
  ;
  border-width: 2px;
  border-style: solid;
}

/* Styles for the modal container */
.modal-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* Semi-transparent background to darken the content */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100; /* Make sure the modal is above other elements */
}

  /* Styles for the modal content */
.confirmation-modal {
    background: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
}

</style>