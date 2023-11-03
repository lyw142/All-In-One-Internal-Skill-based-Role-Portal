<template>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="navbar-left">
            <img src="../assets/logo.png" alt="Logo" class="logo" />
            <router-link to="/hrnav" class="nav-link" style="color: white;">Role listing management</router-link>
            <router-link to="/candidates" class="nav-link" style="color: white;">Candidates</router-link>
            <router-link to="/staffnav" class="nav-link" style="color: white;">View roles</router-link>
            <router-link to="/application-history" class="nav-link" style="color: white;">Application History</router-link>
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
        <!--{{ this.hiringmanagers[0] }}-->
        <form @submit.prevent="formconfirmation">

            <!-- Role Name -->
            <div class="row">
                <div class="form-group mb-3 col-4">
                    <label for="roleName">Role Name</label>
                    <input type="text" class="form-control" id="roleName" v-model="Role_Name" required maxlength="20"
                        pattern="[A-Za-z\s]+" title="(Use alphabets only)" />
                </div>
                <!-- Hiring Manager -->
                <div class="form-group mb-3 col-4">
                    <label for="rolehiringmanager">Hiring Manager</label>
                    <select class="form-select" v-model="Hiring_Manager" style="margin-left: 10px;" id="rolehiringmanager"
                        required>
                        <option value="" disabled>Select a Hiring Manager</option>
                        <option v-for="person in this.hiringmanagers" :value="person.Staff_ID">{{
                            person.Staff_FName }} {{ person.Staff_LName }}
                        </option>
                    </select>
                </div>

                <!-- Department -->
                <div class="form-group col-4">
                    <label for="department">Department</label>
                    <input type="text" class="form-control" id="department" v-model="Dept" required maxlength="50"
                        pattern="[A-Za-z\s]+" title="(Use alphabets only)" />
                </div>
            </div>

            <!-- Role Responsibilities -->
            <div class="form-group mb-3">
                <label for="roleResponsibilities">Role Responsibilities</label>
                <textarea class="form-control" id="roleResponsibilities" v-model="Role_Responsibilities" maxlength="1000"
                    pattern="[A-Za-z\s]+" title="(Use alphabets only)" rows="3"></textarea>
            </div>

            <!-- Confirmation modal (initially hidden) -->
            <div class="modal-container" v-if="showConfirmModal">
                <div class="confirmation-modal">
                    <p>Are you sure you want to create this role listing?</p>
                    <button class="btn btn-primary" style="width: 120px; height: 40px; margin-right: 10px;"
                        @click="submitForm">Confirm</button>
                    <button class="btn btn-secondary" style="width: 120px; height: 40px; margin-left: 10px;"
                        @click="cancelcreation">Cancel</button>
                </div>
            </div>
            <!-- Success Modal -->
            <div class="modal-container" v-if="showSuccessModal">
                <div class="confirmation-modal">
                    <p>Role listing successfully created!</p>
                    <button class="btn btn-primary" @click="returntodashboard">Return</button>
                </div>
            </div>

            <!-- Role Requirements -->
            <!-- <div class="form-group mb-3">
                <label for="roleRequirements">Role Requirements</label>
                <textarea class="form-control" id="roleRequirements" v-model="Role_Requirements" required maxlength="1000"
                    pattern="[A-Za-z\s]+" title="(Use alphabets only)" rows="3"></textarea>
            </div> -->
            <!-- Skill -->
            <div class="row">
                <div class="form-group mb-3 col-6">
                    <label for="roleSkills">Skills required</label>
                    <select class="form-select" v-model="selectedSkill" @change="addSkill" style="margin-left: 10px;"
                        id="roleSkills">
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
                <div class="form-group col-6">
                    <label for="country">Country</label>
                    <input type="text" class="form-control" id="country" v-model="this.Country" required maxlength="20"
                        pattern="[A-Za-z\s]+" title="(Use alphabets only)" />
                </div>
            </div>


            <!-- Salary -->
            <div class="form-group mb-3">
                <div class="row">
                    <div class="col-6">
                        <label for="roleSalary">Salary ($ per year)</label>
                        <input type="number" class="form-control" id="roleSalary" :value="Salary"
                            @input="Salary = $event.target.value.toString()" required pattern="[0-9]{1,11}"
                            title="(Use numbers only)" />
                    </div>
                </div>
            </div>
            <div class="row">
                <!-- Date Posted -->
                <div class="form-group mb-3 col-6">
                    <label for="roleDatePosted">Date Posted</label>
                    <input type="date" class="form-control" id="roleDatePosted" v-model="Date_Posted" required />
                </div>
                <!-- Deadline -->
                <div class="form-group mb-3 col-6">
                    <label for="roleDeadline">Deadline</label>
                    <input :style="{ borderColor: this.invalidcolor }" type="date" class="form-control" id="roleDeadline"
                        v-model="Deadline" required />

                    <div id="invaliddate">
                    </div>
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
            showDateModal: false,
            showConfirmModal: false,
            showSuccessModal: false,
            invalidcolor: "",
            hiringmanagers: [],

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
            Country: "",
        };
    },
    methods: {
        submitForm() {

            if (this.Deadline > this.Date_Posted) {
                axios.post('http://127.0.0.1:5000/api/createjoblisting', {
                    Role_Name: this.Role_Name,
                    Role_Responsibilities: this.Role_Responsibilities,
                    // Role_Requirements: this.Role_Requirements,
                    Dept: this.Dept,
                    Salary: this.Salary,
                    Skills: this.selectedSkills,
                    Deadline: this.Deadline,
                    Date_Posted: this.Date_Posted,
                    Hiring_Manager: this.Hiring_Manager,
                    Country: this.Country,
                }).then(response => {
                    console.log(response);
                    this.showConfirmModal = false;
                    this.showSuccessModal = true;
                });
            } else {
                this.checkDatevalid();
                this.showConfirmModal = false;
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
        },
        checkDatevalid() {
            let invaliddatetext = document.getElementById("invaliddate");
            if (this.Deadline < this.Date_Posted) {
                invaliddatetext.innerText = "Deadline cannot be before or on the date that this role listing was created."
                this.invalidcolor = 'red'
                return false
            }
            else {
                return true
            }
        },
        formconfirmation() {
            this.showConfirmModal = true;
        },
        cancelcreation() {
            this.showConfirmModal = false;
        },
        returntodashboard() {
            this.$router.push("/hrnav");
        }

    },
    mounted() {
        this.getUserSessionData();
        axios.get('http://127.0.0.1:5000/api/skills').then(response => this.availableSkills = response.data)
        axios.get('http://127.0.0.1:5000/api/getstaffwithaccess>3').then(response => this.hiringmanagers = response.data)

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

/* Styles for the modal content */
.confirmation-modal {
    background: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
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
</style>