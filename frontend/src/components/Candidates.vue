<template>
  <div>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
      <div class="navbar-left">
        <img src="../assets/logo.png" alt="Logo" class="logo" />
        <a to="/roles" class="nav-link" style="color: white">Roles</a>
        <a to="/candidates" class="nav-link" style="color: white">Candidates</a>
        <a to="/view-staff-skills" class="nav-link" style="color: white"
          >View Staff Skills</a
        >
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
            <option v-for="role in roles" :value="role">{{ role }}</option>
          </select>
        </div>
      </div>
      <button v-if="selectedRole" class="btn btn-success mb-4">
        Applicants ({{ applicationCount }})
      </button>

      <!-- Table to display candidate information -->
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Name</th>
            <th>Date of Application</th>
            <th>Skills</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="candidate in sortedCandidates">
            <td>{{ candidate.Staff_FName }}</td>
            <td>Applied {{ formatDate(candidate.Application_Date) }}</td>
            <td style="max-width: 300px">
              <span
                v-for="skill in candidate.Skills"
                :key="skill.Skill_Name"
                class="skill-box"
              >
                {{ skill.Skill_Name }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // Import Axios library

export default {
  data() {
    return {
      applications: [],
      roles: [], // Array to store unique roles
      selectedRole: "", // Selected role from the dropdown
      applicationCount: 0, // Number of applications for the selected role
    };
  },
  computed: {
    // Compute a sorted list of candidates based on the date of application
    sortedCandidates() {
      return this.applications
        .filter(
          (app) => !this.selectedRole || app.Role_Name === this.selectedRole
        )
        .sort(
          (a, b) => new Date(a.Application_Date) - new Date(b.Application_Date)
        );
    },
  },
  mounted() {
    // Fetch applications from your API and populate roles array
    this.fetchApplications();
  },
  methods: {
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

    fetchApplications() {
      const apiUrl = `http://127.0.0.1:5000/api/getapplications`;

      axios.get(apiUrl).then((response) => {
        const applications = response.data;
        this.applications = applications;
        // Extract unique roles from applications and store them in the roles array
        this.roles = Array.from(
          new Set(applications.map((app) => app.Role_Name))
        );
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
        }
      });
    },
    countApplications() {
      // Count the number of applications for the selected role
      if (this.selectedRole) {
        const selectedRole = this.selectedRole;
        console.log(this.selectedRole);
        const filteredApplications = this.applications.filter(
          (app) => app.Role_Name === selectedRole
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
