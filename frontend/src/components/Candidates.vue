<template>
  <div>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
      <!-- ... Navbar content ... -->
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
      <div class="row mb-4">
        <!-- Column for the button -->
        <div class="col-md-10">
          <button v-if="selectedRole" class="btn btn-success">
            Applicants ({{ applicationCount }})
          </button>
        </div>

        <!-- Column for the "Order By" dropdown -->
        <div class="col-md-2">
          <div class="dropdown">
            <button class="btn btn-primary dropdown-toggle" type="button" id="skillsDropdown" data-bs-toggle="dropdown"
              aria-haspopup="true" aria-expanded="false">
              Order By
            </button>
            <div class="dropdown-menu" aria-labelledby="skillsDropdown" @click.stop>
              <!-- Checklist of skills with checkboxes -->
              <div class="skills-scroll">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="selectedOrderBy" value="SkillCount" class="checkbox-input" @click="showTable"/>
                  <span class="checkbox-text"> Skill Count</span>
                </label>
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
        <tbody>
          <!-- Use a computed property to sort candidates based on the selected order -->
          <tr v-if="sortOrder == true" v-for="candidate in sortedCandidates" :key="candidate.Staff_FName" v-show="true">
            <td>{{ candidate.Staff_FName }}</td>
            <td>Applied {{ formatDate(candidate.Application_Date) }}</td>
            <td style="max-width: 300px">
              <span v-for="skill in candidate.Skills" :key="skill.Skill_Name" class="skill-box">
                {{ skill.Skill_Name }}
              </span>
            </td>
          </tr>
          <tr v-if="sortCount == true" v-for="(application, id) in applicationsforCount" :key="id">
            <td>{{ application.Staff_Name }}</td>
            <td>{{ application.Application_Status }} {{ formatDate(application.Application_Date) }}</td>
            <td style="max-width: 300px">
              <span v-for="skill in application.Skill" :key="skill.Staff_ID" class="skill-box">
                {{ skill }}
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
import Cookies from 'js-cookie'

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
    }
  },
  mounted() {
    this.getUserSessionData();
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
          this.Listing_ID = application.Listing_ID;
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
          console.log(this.getApplicantBySkillCount())
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
    // Clear user session data from the cookie
    clearUserSessionData() {
      Cookies.remove('userSession');
      this.$router.push("/");; // No user session data found
    },

    getApplicantBySkillCount() {
      const apiUrl = `http://127.0.0.1:5000/api/getApplicantsBySkillMatch/${this.Listing_ID}`;

      axios.get(apiUrl)
        .then((response) => {
          // Handle the response here
          //this.candidates = response.data; // Update your data property with the fetched applicants
          console.log(response.data);
          const applicationsArray = Object.values(response.data);
          this.applicationsforCount = applicationsArray.reverse();
        })
        .catch((error) => {
          // Handle any error that may occur during the request
          console.error('Error fetching data:', error);
        });
    },
    showTable() {
      if(this.selectedOrderBy) {
        this.sortCount = false;
        this.sortOrder = true;
      }
      else {
        this.sortCount = true;
        this.sortOrder = false;
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
</style>
