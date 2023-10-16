<template>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="navbar-left">
            <img src="../assets/logo.png" alt="Logo" class="logo" />
            <a to="/roles" class="nav-link" style="color: white;">Roles</a>
            <a to="/candidates" class="nav-link" style="color: white;">Candidates</a>
            <a to="/view-staff-skills" class="nav-link" style="color: white;">View Staff Skills</a>
        </div>
        <div class="navbar-right">
            <button class="btn btn-secondary" @click="clearUserSessionData()">Logout</button>
        </div>
    </div>
    <!-- form starts here -->

    <div class="container mt-4">

        <div style="display: flex; align-items: center;margin-bottom: 20px;">
            <button type="button" class="btn" @click="cancel" style="padding: 0; margin: 0;">
                <img src="../assets/images/backbtn.png" alt="Back" class="logo" style="margin-right: 0;" />
            </button>
            <h1 style="margin-bottom: 0; margin-left: 10px;">Create a new role listing</h1>
        </div>

        <form @submit.prevent="submitForm">

            <!-- Role Name -->
            <div class="row">
                <div class="form-group mb-3 col-5">
                    <label for="roleName">Role Name</label>
                    <input type="text" class="form-control" id="roleName" v-model="Role_Name" required maxlength="20"
                        pattern="[A-Za-z\s]+" />
                </div>
                <!-- Hiring Manager -->
                <div class="form-group mb-3 col-5">
                    <label for="roleHiringManager">Hiring Manager</label>
                    <input type="text" class="form-control" id="roleHiringManager" v-model="Hiring_Manager" required
                        maxlength="20" pattern="[0-9]{1,11}" />
                </div>
                <!-- Department -->
                <div class="form-group col-2">
                    <label for="department">Department</label>
                    <input type="text" class="form-control" id="department" v-model="Dept" required maxlength="50"
                        pattern="[A-Za-z\s]+" />
                </div>
            </div>

            <!-- Role Responsibilities -->
            <div class="form-group mb-3">
                <label for="roleResponsibilities">Role Responsibilities</label>
                <textarea class="form-control" id="roleResponsibilities" v-model="Role_Responsibilities" required
                    maxlength="1000" pattern="[A-Za-z\s]+" rows="6"></textarea>
            </div>

            <!-- Role Requirements -->
            <div class="form-group mb-3">
                <label for="roleRequirements">Role Requirements</label>
                <textarea class="form-control" id="roleRequirements" v-model="Role_Requirements" required maxlength="1000"
                    pattern="[A-Za-z\s]+" rows="6"></textarea>
            </div>
            <!-- Skill -->
            <div class="form-group mb-3">
                <label for="roleSkills">Skills required</label>
                <select v-model="selectedSkill" @change="addSkill" style="margin-left: 10px;">
                    <option value="" disabled>Select a skill</option>
                    <option v-for="skill in this.availableSkills" :key="skill.Skill_ID" :value="skill.Skill_Name">{{
                        skill.Skill_Name }}
                    </option>
                </select>
                <ul style="margin-top: 5px;">
                    <li class="skill-box mb-2" v-for="(skill, index) in selectedSkills" :key="index">
                        {{ skill }}
                        <button @click="removeSkill(index)" style="border: none; background: none; cursor: pointer;">
                            <img src="../assets/images/closeicon.png" alt="Remove"
                                style="border-radius: 5px; width: 15px; height: 15px;">
                        </button>
                    </li>
                </ul>
            </div>

            <!-- Salary -->
            <div class="form-group mb-3">
                <div class="row">
                    <div class="col-6">
                        <label for="minSalary">Salary ($)</label>
                        <input type="number" class="form-control" id="roleSalary" :value="Salary"
                            @input="Salary = $event.target.value.toString()" required pattern="[0-9]{1,11}" />
                    </div>
                </div>
            </div>
            <div class="row">
                <!-- Deadline -->
                <div class="form-group mb-3 col-6">
                    <label for="roleDeadline">Deadline</label>
                    <input type="date" class="form-control" id="roleDeadline" v-model="Deadline" required />
                </div>

                <!-- Date Posted -->
                <div class="form-group mb-3 col-6">
                    <label for="roleDatePosted">Date Posted</label>
                    <input type="date" class="form-control" id="roleDatePosted" v-model="Date_Posted" required />
                </div>
            </div>
            <button type="submit" class="btn btn-secondary">Submit</button>
            <button type="button" class="btn btn-secondary" @click="cancel" style="margin-left: 20px;">Cancel</button>
        </form>
    </div>
</template>
  
  
<script>
import axios from 'axios'
import Cookies from 'js-cookie'
export default {
    data() {
        return {
            // variables that i used 
            selectedSkill: '',
            selectedSkills: [],
            availableSkills: [],

            // for form submission
            Role_Name: "",
            Role_Responsibilities: "",
            Role_Requirements: "",
            Dept: "",
            Salary: "",
            Skills: [],
            Deadline: "",
            Date_Posted: "",
            Hiring_Manager: "",

        };
    },
    methods: {
        submitForm() {
            if (this.Deadline > this.Date_Posted) {
                axios.post('http://127.0.0.1:5000/api/createjoblisting', {
                    Role_Name: this.Role_Name,
                    Role_Responsibilities: this.Role_Responsibilities,
                    Role_Requirements: this.Role_Requirements,
                    Dept: this.Dept,
                    Salary: this.Salary,
                    Skills: this.Skills,
                    Deadline: this.Deadline,
                    Date_Posted: this.Date_Posted,
                    Hiring_Manager: this.Hiring_Manager,
                }).then(response => {
                    console.log(response);
                    alert("New role listing successfully created");
                    this.$router.push("/hrnav");
                });
            } else {
                // Display an alert if the deadline is before or equal to the date_created
                alert("Deadline cannot be before or on the the same date as Date Posted");
            }

        },
        cancel() {
            this.$router.push("/hrnav");
        },
        addSkill() {
            if (this.selectedSkill && !this.selectedSkills.includes(this.selectedSkill)) {
                this.selectedSkills.push(this.selectedSkill);
                this.selectedSkill = ''; // Clear the selected skill after adding
            }
        },
        removeSkill(index) {
            this.selectedSkills.splice(index, 1);
        },
        // Retrieve user session data from a cookie
        getUserSessionData() {
            const serializedUser = Cookies.get('userSession')
            if (serializedUser) {
                const data = JSON.parse(serializedUser)
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
        }
    },
    mounted() {
        this.getUserSessionData();
        axios.get('http://127.0.0.1:5000/api/skills').then(response => this.availableSkills = response.data)
    }
};
</script>
  
<style scoped>
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


.skill-box {
    display: inline-block;
    background-color: rgba(25, 135, 84, 0.1);
    padding: 4px 8px;
    margin-right: 5px;
    margin-bottom: 5px;
    border-radius: 4px;
    font-size: 14px;
}

form {
    margin-bottom: 20px;
}
</style>