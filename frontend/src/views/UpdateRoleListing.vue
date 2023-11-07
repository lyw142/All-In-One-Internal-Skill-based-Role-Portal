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
            <h1 style="margin-bottom: 0; margin-left: 10px;">Update role listing</h1>
        </div>
        <form @submit.prevent="formconfirmation">

            <!-- Role Responsibilities -->
            <div class="form-group mb-3">
                <label for="roleResponsibilities">Role Responsibilities</label>
                <textarea class="form-control" id="roleResponsibilities" v-model="this.Role_Responsibilities" required
                    maxlength="1000" pattern="[A-Za-z\s]+" title="(Use alphabets only)" rows="4"></textarea>
            </div>

            <!-- Confirmation modal (initially hidden) -->
            <div class="modal-container" v-if="showConfirmModal">
                <div class="confirmation-modal">
                    <p>Are you sure you want to update this role listing?</p>
                    <button class="btn btn-primary" style="width: 120px; height: 40px; margin-right: 10px;"
                        @click="submitForm">Confirm</button>
                    <button class="btn btn-secondary" style="width: 120px; height: 40px; margin-left: 10px;"
                        @click="cancelcreation">Cancel</button>
                </div>
            </div>
            <!-- Success Modal -->
            <div class="modal-container" v-if="showSuccessModal">
                <div class="confirmation-modal">
                    <p>Role listing successfully updated!</p>
                    <button class="btn btn-primary" @click="cancel">Return</button>
                </div>
            </div>
            <!-- Skill -->
            <div class="row">
                <div class="form-group col-6">
                    <label for="roleSkills">Skills required</label>
                    <select class="form-select" v-model="selectedSkill" @change="addSkill" style="margin-left: 10px;">
                        <option value="" disabled>Select a skill</option>
                        <option v-for="skill in this.availableSkills" :key="skill.Skill_ID" :value="skill.Skill_Name">{{
                            skill.Skill_Name }}</option>
                    </select>
                    <ul style="margin-top: 5px;">
                        <li class="skill-box mb-2" v-for="skill in selectedSkills" :key="skill">
                            {{ skill }}

                            <button @click="removeSkill(skill)" style="border: none; background: none; cursor: pointer;">
                                <img src="../assets/images/closeicon.png" alt="Remove"
                                    style="border-radius: 5px; width: 15px; height: 15px;">
                            </button>

                        </li>
                    </ul>
                </div>

                <div class="form-group col-6">
                    <label for="department">Country</label>
                    <select class="form-select" v-model="this.Country" id="country" required>
                        <option value="" disabled>Select a Country</option>
                        <option v-for="countryName in this.CountryList" :value="countryName">{{ countryName }}</option>
                    </select>
                </div>
            </div>


            <!-- Salary -->
            <div class="form-group">
                <div class="row">
                    <div class="form-group mb-3 col-6">
                        <label for="roleDatePosted">Date Posted</label>
                        <input type="date" class="form-control" id="roleDatePosted" v-model="Date_Posted" required />
                    </div>
                    <div class="form-group mb-3 col-6">
                        <label for="roleDeadline">Deadline</label>
                        <input :style="{ borderColor: this.invalidcolor }" type="date" class="form-control"
                            id="roleDeadline" v-model="Deadline" required />

                        <div id="invaliddate">
                        </div>
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-secondary">Update</button>
            <button type="button" class="btn btn-secondary" @click="cancel" style="margin-left: 20px;">Cancel</button>
        </form>
    </div>
</template>
  
  
<script>
import axios from 'axios'
import Cookies from 'js-cookie'

export default {
    props: ['Listing_ID'],
    data() {
        return {
            selectedSkill: '',
            selectedSkills: [],
            availableSkills: [],
            originalSkills: [],
            addedSkills: [],
            removedSkills: [],
            addedSkills_ID: [],
            removedSkills_ID: [],
            invalidcolor: "",
            showDateModal: false,
            showConfirmModal: false,
            showSuccessModal: false,

            Role_Responsibilities: "",
            Skills: [],
            Deadline: "",
            Country: "",
            Date_Posted: "",
            CountryList: []

        };
    },
    methods: {
        cancel() {
            this.$router.push("/hrnav");
        },
        addSkill() {
            if (this.selectedSkill && !this.selectedSkills.includes(this.selectedSkill)) {
                this.selectedSkills.push(this.selectedSkill);
                this.selectedSkill = '';

            }
        },
        removeSkill(skillToRemove) {
            const index = this.selectedSkills.indexOf(skillToRemove);
            if (index !== -1) {
                this.selectedSkills.splice(index, 1);
            }

        },
        compareSkills() {
            this.addedSkills = this.selectedSkills.filter(skill => !this.originalSkills.includes(skill));
            this.removedSkills = this.originalSkills.filter(skill => !this.selectedSkills.includes(skill));
            console.log(this.addedSkills);
            console.log(this.removedSkills);
        },

        submitForm() {
            this.compareSkills();
            if (this.addedSkills.length > 0) {
                this.addedSkills.forEach((skillName) => {
                    // Find the skill in skillDatabase by matching the Skill_Name.
                    const matchingSkill = this.availableSkills.find((skill) => skill.Skill_Name === skillName);

                    // If a matching skill is found, add its Skill_ID to the added skills array.
                    if (matchingSkill) {
                        this.addedSkills_ID.push(matchingSkill.Skill_ID);
                    }
                });
            };
            if (this.removedSkills.length > 0) {
                this.removedSkills.forEach((skillName) => {
                    // Find the skill in skillDatabase by matching the Skill_Name.
                    const matchingSkill = this.availableSkills.find((skill) => skill.Skill_Name === skillName);

                    // If a matching skill is found, add its Skill_ID to the removed skills array.
                    if (matchingSkill) {
                        this.removedSkills_ID.push(matchingSkill.Skill_ID);
                    }
                });
            };
            console.log(this.addedSkills_ID);
            console.log(this.removedSkills_ID);
            // post method goes here 
            const url = `http://127.0.0.1:5000/api/updateRoleListing/${this.Listing_ID}`;

            // Check if the deadline is after the date_created
            if (this.Deadline > this.Date_Posted) {
                axios.put(url, {
                    Role_Responsibilities: this.Role_Responsibilities,
                    Date_Posted: this.Date_Posted,
                    AddedSkills: this.addedSkills_ID,
                    RemovedSkills: this.removedSkills_ID,
                    Deadline: this.Deadline,
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
        checkDatevalid() {
            let invaliddatetext = document.getElementById("invaliddate");
            invaliddatetext.innerText = "Deadline cannot be before or on the date that this role listing was created."
            this.invalidcolor = 'red'
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
        formconfirmation() {
            this.showConfirmModal = true;
        },
        cancelcreation() {
            this.showConfirmModal = false;
        }
    },
    mounted() {
        this.getUserSessionData();
        axios.get('http://127.0.0.1:5000/api/getUniqueCountry').then(response => this.CountryList = response.data)
        const apiUrl = `http://127.0.0.1:5000/api/getRoleListing/${this.Listing_ID}`;
        axios.get(apiUrl).then(response => {
            this.Role_Responsibilities = response.data[0].Role_Responsibilities;
            this.Deadline = response.data[0].Deadline;
            this.Country = response.data[0].Country;
            this.selectedSkills = response.data[0].Skills;
            this.Date_Posted = response.data[0].Date_Posted;
            // this.originalSkills = response.data[0].Skills;
        });
        axios.get('http://127.0.0.1:5000/api/skills').then(response => this.availableSkills = response.data)
    },
    created() {
        const apiUrltwo = `http://127.0.0.1:5000/api/getRoleListing/${this.Listing_ID}`;
        axios.get(apiUrltwo).then(response => {
            this.originalSkills = response.data[0].Skills;
        });
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