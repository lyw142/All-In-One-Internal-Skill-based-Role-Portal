<template>
  <div>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
      <div class="navbar-left">
        <img src="../assets/logo.png" alt="Logo" class="logo" />
        <router-link to="/hrnav" class="nav-link" style="color: white">Role listing management</router-link>
        <router-link to="/candidates" class="nav-link" style="color: white">Candidates</router-link>
        <router-link to="/staffnav" class="nav-link" style="color: white">View roles</router-link>
        <router-link to="/application-history" class="nav-link" style="color: white">Application History</router-link>
      </div>
      <div class="navbar-right">
        <button class="btn btn-secondary" @click="clearUserSessionData()">
          Logout
        </button>
      </div>
    </div>
    <div class="container">
      <div class="col-5 mb-4">
        <div class="form-group role-form">
          <label for="roleDropdown">Role:</label>
          <select id="roleDropdown" class="form-control" v-model="selectedRole">
            <option v-for="role in roles" :value="role">
              {{ role.Role_Name }} (Job Listing ID: {{ role.Listing_ID }})
            </option>
          </select>
        </div>
      </div>
      <div class="row mb-4">
        <!-- Column for the "Applicants" button on the left -->
        <div class="col-md-8">
          <button v-if="selectedRole" class="btn btn-success">
            Applicants ({{ applicationCount }})
          </button>
        </div>

        <!-- Column for the "Order By" dropdown on the right -->
        <div class="col-md-2 text-end" style="padding-right: 0;">
          <div class="dropdown">
            <button class="btn btn-primary dropdown-toggle" type="button" id="skillsDropdown" data-bs-toggle="dropdown"
              aria-haspopup="true" aria-expanded="false">
              Order By
            </button>
            <div class="dropdown-menu" aria-labelledby="skillsDropdown" @click.stop>
              <!-- Checklist of skills with checkboxes -->
              <div class="skills-scroll">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="selectedOrderBy" value="SkillCount" class="checkbox-input"
                    @click="showTable" />
                  <span class="checkbox-text"> Skill Count</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Column for the "Filter by Skills" dropdown on the right -->
        <div class="col-md-2 text-end">
          <div class="dropdown">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="skillsDropdown" data-bs-toggle="dropdown"
              aria-haspopup="true" aria-expanded="false">
              Filter by Skills
            </button>
            <div class="dropdown-menu" aria-labelledby="skillsDropdown" @click.stop>
              <!-- Checklist of skills with checkboxes -->
              <div class="skills-scroll">
                <div v-for="(skill, index) in availableSkills" :key="skill.Skill_ID">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="selectedSkillstemp" :value="skill.Skill_Name"
                      class="checkbox-input" />
                    <span class="checkbox-text">{{ skill.Skill_Name }}</span>
                  </label>
                </div>
              </div>
              <div class="filter-buttons">
                <button class="btn btn-primary" @click="applyFilter">Show Results</button>
                <button class="btn btn-secondary" @click="clearFilter">Clear Filter</button>
              </div>
              <div class="filter-message" v-if="showNoSkillsMessage">
                {{ showNoSkillsMessage }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Table to display candidate information -->
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Name</th>
            <th>Date of Application</th>
            <th>Skills</th>
          </tr>
        </thead>
        <tbody v-if="this.selectedSkills.length == 0">
          <!-- Use a computed property to sort candidates based on the selected order -->
          <tr v-if="sortOrder == true" v-for="candidate in sortedCandidates" :key="candidate.Staff_FName" v-show="true">
            <td class="clickable" @click="openModal(candidate)">
              {{ candidate.Staff_FName }} {{ candidate.Staff_LName }}
            </td>
            <td>Applied {{ formatDate(candidate.Application_Date) }}</td>
            <td style="max-width: 300px" v-if="candidate.roleListing">
              <span v-for="skill in candidate.roleListing.Skills" :key="skill" class="skill-box"
                :class="{ disabled: !checkMatch(candidate, skill) }">
                {{ checkSkillMatch(candidate, skill) }} {{ skill }}
              </span>
            </td>
          </tr>
          <tr v-if="sortCount == true" v-for="(application, id) in applicationsforCount" :key="id">
            <td class="clickable" @click="openModal(application)">{{ application.Staff_FName }} {{ application.Staff_LName }}</td>
            <td>
              Applied
              {{ formatDate(application.Application_Date) }}
            </td>
            <td style="max-width: 300px">
              <span v-for="skill in application.roleListing.Skills" :key="skill" class="skill-box"
                :class="{ disabled: !checkMatch(application, skill) }">
                {{ checkSkillMatch(application, skill) }} {{ skill }}
              </span>
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr v-for="candidate in filteredCandidates" :key="candidate.Staff_FName" v-show="true">
            <td class="clickable" @click="openModal(candidate)">
              {{ candidate.Staff_FName }} {{ candidate.Staff_LName }}
            </td>
            <td>Applied {{ formatDate(candidate.Application_Date) }}</td>
            <td style="max-width: 300px">
              <span v-for="skill in candidate.roleListing.Skills" :key="skill" class="skill-box"
                :class="{ disabled: !checkMatch(candidate, skill) }">
                {{ checkSkillMatch(candidate, skill) }} {{ skill }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="modal" v-if="selectedCandidate" @click="closeModal">
    <div class="modal-content" @click.stop>
      <span class="close" @click="closeModal">&times;</span>
      <h3>
        {{ selectedCandidate.Staff_FName }} {{ selectedCandidate.Staff_LName }}
      </h3>
      <p>
        <strong>Full Name:</strong> {{ selectedCandidate.Staff_FName }}
        {{ selectedCandidate.Staff_LName }}
      </p>
      <p>
        <strong>Current Job:</strong>
        {{ selectedCandidate.Staff_Current_Role }}
      </p>
      <p>
        <strong>Skills:</strong>
        <span v-for="skill in selectedCandidate.Skills" :key="skill.Skill_Name" class="skill-box">
          {{ skill.Skill_Name }}
        </span>
      </p>
      <p>
        <strong>% of Skills matched</strong>
      <div class="progress">
        <div class="progress-bar" role="progressbar" :style="{
          width: getPercentageSkillsMatched(selectedCandidate) + '%',
        }">
          {{ Math.round(getPercentageSkillsMatched(selectedCandidate)) }}%
        </div>
      </div>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // Import Axios library
import Cookies from "js-cookie";

export default {
  data() {
    return {
      applications: [],
      applicationsforCount: [],
      roles: [], // Array to store unique roles
      selectedRole: "", // Selected role from the dropdown
      applicationCount: 0, // Number of applications for the selected role
      selectedOrderBy: false,
      Listing_ID: 0,
      sortOrder: true,
      sortCount: false,
      availableSkills: null,
      selectedSkills: [],
      selectedSkillstemp: [],
      showNoSkillsMessage: "",
      rolecandidates: null,
      selectedCandidate: null,
    };
  },
  computed: {
    // Compute a sorted list of candidates based on the date of application
    sortedCandidates() {
      this.rolecandidates = this.applications
        .filter(
          (app) =>
            !this.selectedRole || app.Listing_ID === this.selectedRole.Listing_ID
        )
        .sort(
          (a, b) => new Date(a.Application_Date) - new Date(b.Application_Date)
        );
        this.getApplicantBySkillCount();
        this.countApplications();
      return this.rolecandidates;
    },
    filteredCandidates() {
      return this.rolecandidates.filter((candidate) => {
        return this.selectedSkills.every((skill) => {
          return candidate.Skills.some(
            (candidateSkill) => candidateSkill.Skill_Name === skill
          );
        });
      });
    },
  },
  mounted() {
    this.getUserSessionData();
    // Fetch applications from your API and populate roles array
    this.fetchApplications();
    this.fetchSkills();
  },
  methods: {
    checkMatch(candidate, skillName) {
      const candidateSkills = candidate.Skills;

      // Check if the skillName exists in the candidateSkills array
      const isSkillMatch = candidateSkills.some(
        (skill) => skill.Skill_Name === skillName
      );
      return isSkillMatch;
    },
    checkSkillMatch(candidate, skillName) {
      // Retrieve the skills from the job listing
      const candidateSkills = candidate.Skills;

      // Check if the skillName exists in the candidateSkills array
      const isSkillMatch = candidateSkills.some(
        (skill) => skill.Skill_Name === skillName
      );

      // Return "✓" for a match and "✗" for no match
      return isSkillMatch ? "✓" : "✗";
    },
    getPercentageSkillsMatched(candidate) {
      console.log({ candidate });
      const totalSkills = candidate.roleListing.Skills.length;
      const matchedSkills = candidate.Skills.filter((candidateSkill) => {
        return candidate.roleListing.Skills.some((roleSkill) => {
          return roleSkill === candidateSkill.Skill_Name;
        });
      }).length;
      return (matchedSkills / totalSkills) * 100;
    },
    fetchApplications() {
      const apiUrl = `http://127.0.0.1:5000/api/getapplications`;

      axios.get(apiUrl).then((response) => {
        const applications = response.data;
        this.applications = applications;
        // Extract unique roles from applications and store them in the roles array
        const uniqueRoles = Array.from(
          new Set(applications.map((app) => app.Listing_ID))
        );

        // Create a roles array with listing ID information
        this.roles = uniqueRoles.map((Listing_ID) => {
          const matchingApp = applications.find(
            (app) => app.Listing_ID === Listing_ID
          );
          return {
            Role_Name: matchingApp.Role_Name,
            Listing_ID: Listing_ID,
          };
        });
        applications.forEach((application) => {
          this.fetchRoleListing(application.Listing_ID);
        });

        this.selectedRole = this.roles[0];
        this.countApplications();
      });
    },
    fetchRoleListing(Listing_ID) {
      const apiUrl = `http://127.0.0.1:5000/api/getRoleListing/${Listing_ID}`;

      axios.get(apiUrl).then((response) => {
        const matchingApps = this.applications.filter(
          (app) => app.Listing_ID === Listing_ID
        );
        if (matchingApps.length > 0) {
          matchingApps.forEach((matchingApp) => {
            matchingApp.roleListing = response.data[0];
          });
          // console.log(this.getApplicantBySkillCount());
        }
      });
    },
    countApplications() {
      // Count the number of applications for the selected role
      if (this.selectedRole) {
        const selectedRole = this.selectedRole.Listing_ID;
        const filteredApplications = this.applications.filter(
          (app) => app.Listing_ID === selectedRole
        );
        this.applicationCount = filteredApplications.length;
      } else {
        this.applicationCount = 0; // If "All Roles" is selected
      }
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    // Retrieve user session data from a cookie
    getUserSessionData() {
      const serializedUser = Cookies.get("userSession");
      if (serializedUser) {
        const data = JSON.parse(serializedUser);
        this.staff_id = data.Staff_ID;
        if (!(data.Access_Rights == 4)) {
          this.$router.push("/staffnav");
        }
      } else {
        this.$router.push("/"); // No user session data found
      }
    },
    // Clear user session data from the cookie
    clearUserSessionData() {
      Cookies.remove("userSession");
      this.$router.push("/"); // No user session data found
    },

    getApplicantBySkillCount() {
      const apiUrl = `http://127.0.0.1:5000/api/getApplicantsBySkillMatch/${this.selectedRole.Listing_ID}`;

      axios
        .get(apiUrl)
        .then((response) => {
          // Handle the response here
          //this.candidates = response.data; // Update your data property with the fetched applicants
          const applicationsArray = Object.values(response.data);
          this.applicationsforCount = applicationsArray;
        })
        .catch((error) => {
          // Handle any error that may occur during the request
          console.error("Error fetching data:", error);
        });
    },
    showTable() {
      if (this.selectedOrderBy) {
        this.sortCount = false;
        this.sortOrder = true;
      } else {
        this.sortCount = true;
        this.sortOrder = false;
      }
    },
    fetchSkills() {
      axios
        .get("http://127.0.0.1:5000/api/skills")
        .then((response) => {
          this.availableSkills = response.data;
        })
        .catch((error) => {
          console.error("Error fetching skills:", error);
        });
    },
    openModal(candidate) {
      this.selectedCandidate = candidate;
    },
    closeModal() {
      this.selectedCandidate = null;
    },
    applyFilter() {
      if (this.selectedSkillstemp.length === 0) {
        // Display a message indicating that at least one skill should be selected
        this.showNoSkillsMessage = 'Please select at least one skill.';
      } else {
        this.selectedSkills = this.selectedSkillstemp;
        this.showNoSkillsMessage = "";
      }
    },
    clearFilter() {
      if (this.selectedSkillstemp.length === 0) {
        // Display a message indicating that at least one skill should be selected
        this.showNoSkillsMessage = 'No skills selected.';
      } else {
        this.selectedSkills = [];
        this.selectedSkillstemp = [];
        this.showNoSkillsMessage = "";
      }
    }
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

/* filter by skills style  */
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

  .skills-scroll {
    max-height: 300px;
    /* Set the maximum height for the dropdown */
    overflow-y: auto;
    /* Enable vertical scrolling if the content exceeds the max height */
    /* Added padding to the modal */
  }
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

.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 60%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.disabled {
  background-color: #6c757d;
  color: white;
}

.clickable {
  color: rgba(25, 135, 84, 1);
  text-decoration: underline;
}

.clickable:hover {
  cursor: pointer;
}

/* Define the progress bar container */
.progress {
  height: 20px;
  /* Set the height of the progress bar */
  background-color: #ccc;
  /* Set a background color for the progress bar container */
  border-radius: 10px;
  /* Add some border radius for rounded corners */
}

/* Define the filled part of the progress bar with the specified color */
.progress-bar {
  background-color: rgb(0, 158, 96);
  /* Set the filled color */
  border-radius: 10px;
  /* Match the border radius to the container */
  transition: width 0.3s ease-in-out;
  /* Add a smooth transition for width changes */
  text-align: center;
  /* Center text within the progress bar */
  color: #fff;
  /* Set text color to white for visibility */
  font-weight: bold;
  /* Make the text bold */
  line-height: 20px;
  /* Vertical centering for text */
}
</style>
