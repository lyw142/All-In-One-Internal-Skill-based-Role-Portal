<template>
  <div>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
      <div class="navbar-left">
        <img src="../assets/logo.png" alt="Logo" class="logo" />
        <a to="/roles" class="nav-link" style="color: white;">Roles</a>
      </div>
      <div class="navbar-right">
        <button class="btn btn-secondary">Logout</button>
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
          <div v-for="role in roles" @click="selectRole(role)">
            <div :class="{ 'card': true, 'green-border': role === selectedRole, 'mb-3': true }">
              <div class="card-body">
                <h5 class="card-title">{{ role.Role_Name }}</h5>
                <p class="card-text">
                  <strong>Skills Required:</strong>
                  <span v-for="skill in role.Skills" class="skill-box" :style="{
                    backgroundColor: userSkills.includes(skill.trim()) ? '#50A050' : 'rgba(25, 135, 84, 0.1)',
                    color: userSkills.includes(skill.trim()) ? 'white' : 'inherit'
                  }">
                    {{ skill.trim() }}
                  </span>
                </p>

                <p class="card-text">
                  <strong>Application Deadline:</strong>
                  {{ role.Deadline }}
                </p>
              </div>
            </div>
          </div>
        </div>
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
                  <ul>
                    <li v-for="line in selectedRole.Role_Responsibilities.split('\n')">
                      {{ line }}
                    </li>
                  </ul>
                </div>

                <!-- Role Requirements -->
                <div class="role-requirements">
                  <strong>Role Requirements</strong>
                  <ul>
                    <li v-for="line in selectedRole.Role_Requirements.split('\n')">
                      {{ line }}
                    </li>
                  </ul>
                </div>
              </div>
              <div class="skills">
                <p>
                  <strong>Skills Required:</strong>
                </p>
                <span v-for="skill in selectedRole.Skills" class="skill-box" :style="{
                  backgroundColor: userSkills.includes(skill.trim()) ? '#50A050' : 'rgba(25, 135, 84, 0.1)',
                  color: userSkills.includes(skill.trim()) ? 'white' : 'inherit'
                }">
                  {{ skill.trim() }}
                </span>
              </div>
              <div>
                <button class="btn btn-secondary" style="margin: 10px;">Apply for role</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      searchQuery: "",
      roles: [],
      selectedRole: {},
      isCardClicked: false,
      isActive: false,
      userSkills: ["Java", "Programming", "English"],
    };
  },
  methods: {
    selectRole(role) {
      this.selectedRole = role;
      this.isCardClicked = true;
    },
    toggleActive() {
      this.isActive = !this.isActive;
    }
  },
  mounted() {
    axios.get('http://127.0.0.1:5000/api/joblistings').then(response => this.roles = response.data)
  }
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

.card {
  text-align: left;
}

.green-border {
  border-color: #4e855a;
  border-width: 2px;
  border-style: solid;
}

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

#roledescription {
  height: 75%;
  position: fixed;
  border-color: #4e855a;
  border-width: 2px;
}
</style>

