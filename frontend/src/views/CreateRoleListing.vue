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
    
    <div class="container mt-4">
      <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <button type="button" class="btn" @click="cancel" style="padding: 0; margin: 0;">
          <img src="../assets/images/backbtn.png" alt="Back" class="logo" style="margin-right: 0;" />
        </button>
        <h1 style="margin-bottom: 0; margin-left: 10px;">Create a new role listing</h1>
      </div>
  
      <div>
        <p style="margin-bottom: 10px;">How would you like to create a role listing?</p>
        <!-- Radio button selection for use cases -->
        <div style="margin-bottom: 20px;">
          <div>
            <input type="radio" id="newRole" v-model="selectedUseCase" value="newRole">
            <label for="newRole" style="margin: 5px;">Create a role listing for a new role</label>
          </div>
          <div>
            <input type="radio" id="existingRole" v-model="selectedUseCase" value="existingRole">
            <label for="existingRole" style="margin: 5px;">Use an existing role's details as a template</label>
          </div>
        </div>
      </div>
  
      <!-- Conditionally show the appropriate form -->
      <div v-if="selectedUseCase === 'newRole'">
      <form @submit.prevent="formConfirmation">
        <!-- Role Name -->
        <div class="row">
          <div class="form-group mb-3 col-3">
            <label for="roleName">Role Name</label>
            <input type="text" class="form-control" id="roleName" v-model="newRoleFormData.Role_Name" required maxlength="50" pattern="[A-Za-z\s]+" title="(Use alphabets only)" />
          </div>
          <!-- Hiring Manager -->
          <div class="form-group mb-3 col-3">
            <label for="roleHiringManager">Hiring Manager</label>
            <select class="form-select" v-model="newRoleFormData.Hiring_Manager" style="margin-left: 10px;" id="roleHiringManager" required>
              <option value="" disabled>Select a Hiring Manager</option>
              <option v-for="person in hiringmanagers" :value="person.Staff_ID">{{ person.Staff_FName }} {{ person.Staff_LName }} [{{ person.Dept }}, {{ person.Country }}]</option>
            </select>
          </div>
          <!-- Department -->
          <div class="form-group col-3">
            <label for="department">Department</label>
            <select class="form-select" v-model="newRoleFormData.Dept" id="department" required>
              <option value="" disabled>Select a Department</option>
              <option v-for="department in departments" :value="department">{{ department }}</option>
            </select>
          </div>

            <!-- Country -->
            <div class="form-group mb-3 col-3">
            <label for="country">Country</label>
            <select class="form-select" v-model="newRoleFormData.Country" id="country" required>
              <option value="" disabled>Select a Country</option>
              <option v-for="country in countries" :value="country">{{ country }}</option>
            </select>
          </div>
        </div>

        <!-- Role Responsibilities -->
        <div class="form-group mb-3">
          <label for="roleResponsibilities">Role Responsibilities</label>
          <textarea class="form-control" id="roleResponsibilities" v-model="newRoleFormData.Role_Responsibilities" maxlength="1000" pattern="[A-Za-z\s]" title="(Use alphabets only)" rows="3"></textarea>
        </div>
          <!-- Confirmation modal (initially hidden) -->
          <div class="modal-container" v-if="showConfirmModal">
            <div class="confirmation-modal">
              <p>Are you sure you want to create this role listing?</p>
              <button class="btn btn-primary" style="width: 120px; height: 40px; margin-right: 10px;" @click="submitForm">Confirm</button>
              <button class="btn btn-secondary" style="width: 120px; height: 40px; margin-left: 10px;" @click="cancelCreation">Cancel</button>
            </div>
          </div>
          <!-- Success Modal -->
          <div class="modal-container" v-if="showSuccessModal">
            <div class="confirmation-modal">
              <p>Role listing successfully created!</p>
              <button class="btn btn-primary" @click="returnToDashboard">Return</button>
            </div>
          </div>


        <!-- Skills required -->
        <div class="form-group mb-3">
          <label for="roleSkills">Skills required</label>
          <select class="form-select" v-model="newRoleFormData.selectedSkill" @change="addNewRoleSkill" id="roleSkills">
            <option value="" disabled>Select a skill</option>
            <option v-for="skill in availableSkills" :key="skill.Skill_ID" :value="skill.Skill_Name">{{ skill.Skill_Name }}</option>
          </select>
          <ul style="margin-top: 5px;">
            <li class="skill-box mb-2" v-for="(skill, index) in newRoleFormData.selectedSkills" :key="index">{{ skill }}
                <button @click="removeNewRoleSkill(index)" style="border: none; background: none; cursor: pointer;">
                <img src="../assets/images/closeicon.png" alt="Remove" style="border-radius: 5px; width: 15px; height: 15px;">
              </button>
            </li>
          </ul>
        </div>

        <!-- Date Posted -->
        <div class="row">
          <div class="form-group mb-3 col-6">
            <label for="roleDatePosted">Date Posted</label>
            <input type="date" class="form-control" id="roleDatePosted" v-model="newRoleFormData.Date_Posted" required />
          </div>
          <!-- Deadline -->
          <div class="form-group mb-3 col-6">
            <label for="roleDeadline">Deadline</label>
            <input :style="{ borderColor: invalidcolor }" type="date" class="form-control" id="roleDeadline" v-model="newRoleFormData.Deadline" required />
            <div id="invaliddate"></div>
          </div>
        </div>
        <button type="submit" class="btn btn-secondary">Submit</button>
        <button type="button" class="btn btn-secondary" @click="cancel" style="margin-left: 20px;">Cancel</button>
      </form>
    </div>

    <div v-else-if="selectedUseCase === 'existingRole'">
        <form @submit.prevent="formConfirmation">
        <!-- Role Name (as a dropdown, you should populate it with your data) -->
        <div class="row">
        <div class="form-group mb-3 col-3">
          <label for="roleName">Role Name</label>
          <select class="form-select" v-model="selectedExistingRole" @change="fetchRoleDetails" id="roleName" required>
            <option value="" disabled>Select a Role Name</option>
            <option v-for="role in availableRoles" :value="role.Role_ID">{{ role.Role_Name }}</option>
          </select>
        </div>
        <!-- Hiring Manager -->
        <div class="form-group mb-3 col-3">
          <label for="roleHiringManager">Hiring Manager</label>
          <select class="form-select" v-model="existingRoleFormData.Hiring_Manager" id="roleHiringManager" required>
            <option value="" disabled>Select a Hiring Manager</option>
            <option v-for="person in hiringmanagers" :value="person.Staff_ID">{{ person.Staff_FName }} {{ person.Staff_LName }} [{{ person.Dept }}, {{ person.Country }}]</option>
          </select>
        </div>
        <!-- Department -->
        <div class="form-group mb-3 col-3">
          <label for="department">Department</label>
          <select class="form-select" v-model="existingRoleFormData.Dept" id="department" required>
            <option value="" disabled>Select a Department</option>
            <option v-for="department in departments" :value="department">{{ department }}</option>
          </select>
        </div>

        <!-- Country -->
            <div class="form-group mb-3 col-3">
            <label for="country">Country</label>
            <select class="form-select" v-model="existingRoleFormData.Country" id="country" required>
              <option value="" disabled>Select a Country</option>
              <option v-for="country in countries" :value="country">{{ country }}</option>
            </select>
          </div>
    </div>
        <!-- Role Responsibilities -->
        <div class="form-group mb-3">
          <label for="roleResponsibilities">Role Responsibilities</label>
          <textarea class="form-control" id="roleResponsibilities" v-model="existingRoleFormData.Role_Responsibilities" maxlength="1000" pattern="[A-Za-z\s]" title="(Use alphabets only)" rows="3"></textarea>
        </div>
          <!-- Confirmation modal (initially hidden) -->
          <div class="modal-container" v-if="showConfirmModal">
            <div class="confirmation-modal">
              <p>Are you sure you want to create this role listing?</p>
              <button class="btn btn-primary" style="width: 120px; height: 40px; margin-right: 10px;" @click="submitexistingroleform">Confirm</button>
              <button class="btn btn-secondary" style="width: 120px; height: 40px; margin-left: 10px;" @click="cancelCreation">Cancel</button>
            </div>
          </div>
          <!-- Success Modal -->
          <div class="modal-container" v-if="showSuccessModal">
            <div class="confirmation-modal">
              <p>Role listing successfully created!</p>
              <button class="btn btn-primary" @click="returnToDashboard">Return</button>
            </div>
          </div>

        <!-- Skills required -->
        <div class="form-group mb-3">
          <label for="roleSkills">Skills required</label>
          <select class="form-select" v-model="existingRoleFormData.selectedSkill" @change="addExistingRoleSkill" id="roleSkills">
            <option value="" disabled>Select a skill</option>
            <option v-for="skill in availableSkills" :key="skill.Skill_ID" :value="skill.Skill_ID">{{ skill.Skill_Name }}</option>
          </select>
          <ul style="margin-top: 5px;">
            <li class="skill-box mb-2" v-for="skill in existingRoleFormData.selectedSkills" :key="skill.Skill_ID">{{ skill.Skill_Name }}
              <button @click="removeExistingRoleSkill(skill.Skill_ID)" style="border: none; background: none; cursor: pointer;">
                <img src="../assets/images/closeicon.png" alt="Remove" style="border-radius: 5px; width: 15px; height: 15px;">
              </button>
            </li>
          </ul>
        </div>

        <!-- Date Posted -->
        <div class="row">
          <div class="form-group mb-3 col-6">
            <label for="roleDatePosted">Date Posted</label>
            <input type="date" class="form-control" id="roleDatePosted" v-model="existingRoleFormData.Date_Posted" required />
          </div>
          <!-- Deadline -->
          <div class="form-group mb-3 col-6">
            <label for="roleDeadline">Deadline</label>
            <input :style="{ borderColor: invalidcolor }" type="date" class="form-control" id="roleDeadline" v-model="existingRoleFormData.Deadline" required />
            <div id="invaliddate"></div>
          </div>
        </div>
        <button type="submit" class="btn btn-secondary">Submit</button>
        <button type="button" class="btn btn-secondary" @click="cancel" style="margin-left: 20px;">Cancel</button>
      </form>
    </div>
  </div>
</template>
  
  <script>
  import axios from 'axios'
  import Cookies from 'js-cookie'
  
  export default {
    data() {
  return {
    selectedSkill: '',
    selectedSkills: '',
    availableSkills: [],
    showDateModal: false,
    showConfirmModal: false,
    showSuccessModal: false,
    invalidcolor: "",
    hiringmanagers: [],
    selectedUseCase: 'newRole',
    selectedExistingRole: '',
    availableRoles: [],
    countries: [],
    departments: [],
    Role_Responsibilities: '',

    newRoleFormData: {
      Role_Name: "",
      Role_Responsibilities: "",
      Dept: "",
    //   Salary: "",
      Skills: [],
      Deadline: "",
      Date_Posted: "",
      Hiring_Manager: "",
      Country: "",
      selectedSkills: [],
      selectedSkill: '',
    },
    existingRoleFormData: {
      Role_Name: "",
      Role_Responsibilities: "",
      Dept: "",
    //   Salary: "",
      Skills: [],
      Deadline: "",
      Date_Posted: "",
      Hiring_Manager: "",
      Country: "",
      selectedSkills: [],
      removedSkills: [],
      addSkills: [],
      selectedSkill: '',
      Role_ID: '', // Add a property for storing the listing ID
    },
  };
},


    methods: {
      submitForm() {
        if (this.newRoleFormData.Deadline > this.newRoleFormData.Date_Posted) {
          axios.post('http://127.0.0.1:5000/api/createjoblisting', {
            Role_Name: this.newRoleFormData.Role_Name,
            Role_Responsibilities: this.newRoleFormData.Role_Responsibilities,
            // Role_Requirements: this.Role_Requirements,
            Dept: this.newRoleFormData.Dept,
            // Salary: this.newRoleFormData.Salary,
            Skills: this.newRoleFormData.selectedSkills,
            Deadline: this.newRoleFormData.Deadline,
            Date_Posted: this.newRoleFormData.Date_Posted,
            Hiring_Manager: this.newRoleFormData.Hiring_Manager,
            Country: this.newRoleFormData.Country,
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

      submitexistingroleform() {
  // console.log("Submitting existingRoleForm");
  // console.log("role_id before API call: " + this.existingRoleFormData.Role_ID);
  // console.log("role_id before API call: " + this.existingRoleFormData.Country);
  // console.log("role_id before API call: " + this.existingRoleFormData.Hiring_Manager);
  if (this.existingRoleFormData.Deadline > this.existingRoleFormData.Date_Posted) {
    axios.post('http://127.0.0.1:5000/api/createjoblistingAnother', {
      Deadline: this.existingRoleFormData.Deadline,
      Date_Posted: this.existingRoleFormData.Date_Posted,
      Country: this.existingRoleFormData.Country,
      AddedSkills: this.existingRoleFormData.selectedSkills,
      RemovedSkills: this.existingRoleFormData.removedSkills,
      Role_Responsibilities: this.existingRoleFormData.Role_Responsibilities,
      Role_ID: this.existingRoleFormData.Role_ID,
      Hiring_Manager: this.existingRoleFormData.Hiring_Manager,
    })
    .then(response => {
      // Retrieve the role_listing_id from the response
      const roleListingId = response.data.role_listing_id;
      console.log(roleListingId)

      // Call the updateexistingrole method with the retrieved role_listing_id
      this.updateexistingrole(roleListingId);
      
      this.showConfirmModal = false;
      this.showSuccessModal = true;
    })
    .catch(error => {
      console.error(error);
    });
  } else {
    this.checkDatevalid();
    this.showConfirmModal = false;
  }
},

      cancel() {
        this.$router.push("/hrnav");
      },


      updateexistingrole(roleListingId) {
  axios.put(`http://127.0.0.1:5000/api/updateRoleListing/${roleListingId}`, {
    // Include the data you want to update
    Deadline: this.existingRoleFormData.Deadline,
    Date_Posted: this.existingRoleFormData.Date_Posted,
    Country: this.existingRoleFormData.Country,
    AddedSkills: this.existingRoleFormData.addSkills,
    RemovedSkills: this.existingRoleFormData.removedSkills,
    Role_Responsibilities: this.existingRoleFormData.Role_Responsibilities
  })
  .then(response => {
    console.log(response);
    this.showConfirmModal = false;
    this.showSuccessModal = true;
  })
  .catch(error => {
    console.error(error);
  });
},



    addNewRoleSkill() {
    if (this.newRoleFormData.selectedSkill && !this.newRoleFormData.selectedSkills.includes(this.newRoleFormData.selectedSkillselectedSkill)) {
      this.newRoleFormData.selectedSkills.push(this.newRoleFormData.selectedSkill);
      this.newRoleFormData.selectedSkill = ''; // Clear the selected skill after adding
    }
    },

    removeNewRoleSkill(index) {
        this.newRoleFormData.selectedSkills.splice(index, 1);
    },

    addExistingRoleSkill() {

        if (this.existingRoleFormData.selectedSkill && !this.existingRoleFormData.selectedSkills.includes(this.existingRoleFormData.selectedSkill)) {
          const selectedSkill = this.availableSkills.find(skill => skill.Skill_ID === this.existingRoleFormData.selectedSkill);
          const selectedSkillObj = {
            Skill_ID: this.existingRoleFormData.selectedSkill,
            Skill_Name: selectedSkill.Skill_Name,
          };
          this.existingRoleFormData.addSkills.push(selectedSkill.Skill_ID);
          this.existingRoleFormData.selectedSkills.push(selectedSkillObj);
          
          this.availableSkills = this.availableSkills.filter(skill => skill.Skill_ID !== this.existingRoleFormData.selectedSkill);
          this.existingRoleFormData.selectedSkill = ''; // Clear the selected skill after adding
          // console.log('addSkills array:', this.existingRoleFormData.selectedSkills);
          // console.log('new skills id', this.existingRoleFormData.addSkills)
      }
    },

    removeExistingRoleSkill(skillId) {
      // Find the index of the skill with the matching Skill_ID
      const index = this.existingRoleFormData.selectedSkills.findIndex(skill => skill.Skill_ID === skillId);

      if (index !== -1) {
        // Get the Skill_ID of the skill
        const removedSkillId = this.existingRoleFormData.selectedSkills[index].Skill_ID;
        
        // // Log to the console
        // console.log(`Removed skill with Skill_ID ${removedSkillId}`);

        // Remove the skill at the found index
        this.existingRoleFormData.selectedSkills.splice(index, 1);
        
        // Append the removed skill's Skill_ID to the removedSkills array
        this.existingRoleFormData.removedSkills.push(removedSkillId);

        // // Log to the console
        // console.log('Updated selectedSkills array:', this.existingRoleFormData.selectedSkills);
        // console.log('Removed Skill_ID appended to removedSkills array:', this.existingRoleFormData.removedSkills);
      }
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
          this.$router.push("/"); // No user session data found
        }
      },
      // Clear user session data from the cookie
      clearUserSessionData() {
        Cookies.remove('userSession');
        this.$router.push("/"); // No user session data found
      },
      checkDatevalid() {
        let invaliddatetext = document.getElementById("invaliddate");
        if (this.Deadline < this.Date_Posted) {
          invaliddatetext.innerText = "Deadline cannot be before or on the date that this role listing was created."
          this.invalidcolor = 'red'
          return false
        } else {
          return true
        }
      },
      formConfirmation() {
        this.showConfirmModal = true;
      },
      cancelCreation() {
        this.showConfirmModal = false;
      },
      returnToDashboard() {
        this.$router.push("/hrnav");
      },

    // Fetch role details when a role is selected from the dropdown
fetchRoleDetails() {
  if (this.selectedExistingRole) {
    axios.get(`http://127.0.0.1:5000/api/getRoleDetails/${this.selectedExistingRole}`).then((response) => {
      // Populate the form fields with role details from the response
      console.log('Role details response:', response.data);
      this.existingRoleFormData.Role_Name = response.data.Role_Name;
      this.existingRoleFormData.Role_Responsibilities = response.data.Role_Responsibilities;
      this.existingRoleFormData.Dept = response.data.Dept; // Update this with the correct data field
    //   this.existingRoleFormData.Salary = response.data.Salary; // Update this with the correct data field
      this.existingRoleFormData.Deadline = response.data.Deadline;
      this.existingRoleFormData.Date_Posted = response.data.Date_Posted;
      this.existingRoleFormData.Hiring_Manager = response.data.Hiring_Manager;
      this.existingRoleFormData.Country = response.data.Country;
      this.existingRoleFormData.selectedSkills = response.data.Skills;
      this.existingRoleFormData.Role_ID = response.data.Role_ID;
    });
  }
},
        fetchCreatedRoleDetails() {
    axios.get('http://127.0.0.1:5000/api/getCreatedRoleDetails').then(response => {
        // Populate your data properties with the retrieved role details
        // For example, you can store them in the availableRoles array
        this.availableRoles = response.data;
        
        // Set the selectedRole to the first role in the retrieved roles (or to an appropriate default value)
        if (this.availableRoles.length > 0) {
        this.selectedExistingRole = this.availableRoles[0].Role_ID;

        }
    });
},

},
    mounted() {
      this.getUserSessionData();
      axios.get('http://127.0.0.1:5000/api/skills').then(response => this.availableSkills = response.data)
      axios.get('http://127.0.0.1:5000/api/getstaffwithaccess>3').then(response => this.hiringmanagers = response.data)
      axios.get('http://127.0.0.1:5000/api/getAllRoles').then(response => this.allRoles = response.data)
      axios.get('http://127.0.0.1:5000/api/getAllRoles').then(response => this.availableRoles = response.data)
      //axios.get('http://127.0.0.1:5000/api/getCreatedRoleDetails').then(response => this.availableRoles = response.data)
      axios.get('http://127.0.0.1:5000/api/getUniqueCountry').then(response => this.countries = response.data)
      //axios.get('http://127.0.0.1:5000/api/getUniqueDept').then(response => this.departments = response.data)
      axios.get('http://127.0.0.1:5000/api/getUniqueDept')
        .then(response => {
          const excludedDepartments = ['CEO', 'Chairman']; // Add the names you want to exclude

          this.departments = response.data.filter(department => !excludedDepartments.includes(department));
        })
        .catch(error => {
          // Handle errors here
          this.departments = response.data
        });

      //this.fetchCreatedRoleDetails(); // Fetch created role details

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
