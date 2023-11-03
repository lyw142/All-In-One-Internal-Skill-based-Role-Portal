<template>
  <div>
    <!-- Navbar -->
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
      <div class="navbar-left">
        <img src="../assets/logo.png" alt="Logo" class="logo" />
        <router-link v-if="userPrivileges != 4" to="/staffnav" class="nav-link" style="color: white;">View
          roles</router-link>
        <router-link v-if="userPrivileges != 4" to="/application-history" class="nav-link"
          style="color: white;">Application History</router-link>
        <!-- New link -->
        <router-link v-if="userPrivileges == 4" to="/hrnav" class="nav-link" style="color: white;">Role listing
          management</router-link>
        <router-link v-if="userPrivileges == 4 || userPrivileges == 3" to="/candidates" class="nav-link"
          style="color: white;">Candidates</router-link>
        <router-link v-if="userPrivileges == 4" to="/staffnav" class="nav-link" style="color: white;">View
          roles</router-link>
        <router-link v-if="userPrivileges == 4" to="/application-history" class="nav-link"
          style="color: white;">Application History</router-link>
      </div>
      <div class="navbar-right">
        <button class="btn btn-secondary" @click="clearUserSessionData()">Logout</button>
      </div>
    </div>

    <!-- Main content -->
    <div class="container mt-4">
      <!-- Header -->
      <h2 class="text-left bold-title" style="margin: 40px 20px;">Application History</h2>

      <!-- Check if there are no pending applications -->
      <div v-if="applications.length === 0" class="no-applications-message" style="margin: 40px 20px;">You have no pending
        applications.</div>


      <!-- Vertically stacked list -->
      <div class="application-list">
        <!-- Use v-for to iterate over your API response data -->
        <div v-for="application in applications" :key="application.Application_ID" class="application-item">
          <div class="application-details">
            <div class="application-title">
              {{ application.Role_Name }}
              <span :class="['application-status', application.Application_Status.toLowerCase()]">{{
                application.Application_Status }}</span>
            </div>
            <div class="application-country-salary">
              <div class="application-country">
                <img src="../assets/location.png" alt="Location" class="pin-icon" />
                {{ application.Country }}
              </div>
              <!-- <div class="application-salary">
                  <img src="../assets/suitcase.png" alt="Salary" class="salary-icon" />
                  ${{ application.Salary }} Annually
                </div> -->
            </div>

            <div class="application-date application-date-right">Application Date: {{
              formatDate(application.Application_Date) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  data() {
    return {
      applications: [], // Store your API response here
      staff_id: null, // Store staff ID
      userPrivileges: 2,
    };
  },
  methods: {
    // Retrieve user session data from a cookie
    getUserSessionData() {
      const serializedUser = Cookies.get('userSession');
      if (serializedUser) {
        const userData = JSON.parse(serializedUser);
        this.staff_id = userData.Staff_ID;
        this.userPrivileges = userData.Access_Rights;
      } else {
        this.$router.push("/"); // No user session data found
      }
      console.log(this.staff_id)
    },

    // Clear user session data from the cookie
    clearUserSessionData() {
      Cookies.remove('userSession');
      this.$router.push("/"); // No user session data found
    },

    formatDate(date) {
      // You can format the date as needed here
      return new Date(date).toLocaleDateString();
    },

    fetchApplicationHistory() {
      // Make an API request to retrieve application data and update the applications array
      axios
        .get(`http://127.0.0.1:5000/api/getApplicationHistory/${this.staff_id}`)
        .then((response) => {
          this.applications = response.data;
          console.log('Retrieved application data:', this.applications); // Log retrieved data
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    this.getUserSessionData();
    // Call the method to fetch application history when the component is mounted
    this.fetchApplicationHistory();
  },
};
</script>
  
  
<style scoped>
/* Navbar styles */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
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
  color: #fff;
  font-size: 16px;
}

/* Style for the Application History page content */
.container {
  margin-top: 20px;
}

.bold-title {
  font-weight: bold;
}

/* Header style */
.application-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Individual application item styles */
.application-item {
  width: 95%;
  border-radius: 5px;
  padding: 20px;
  margin: 10px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #f9fafd;
}

.application-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  /* Increase vertical space between title and status */
}

.application-status {
  font-size: 14px;
  border-radius: 5px;
  padding: 5px 10px;
  margin-left: 5px;
}

.application-status.received {
  background-color: #FAF1D1;
  color: #5C3A00;
}

.application-details-line {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
}

.application-country-salary {
  display: flex;
  align-items: center;
}

.application-country {
  display: flex;
  align-items: center;
  margin-right: 20px;
  /* Adjust the spacing as needed */
}

.application-salary {
  display: flex;
  align-items: center;
}

.pin-icon,
.salary-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

.application-date {
  font-size: 14px;
  text-align: right;
  /* Align date to the right */
}
</style>
  