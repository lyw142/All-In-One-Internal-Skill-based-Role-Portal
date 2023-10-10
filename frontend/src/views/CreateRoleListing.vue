<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#"><img src="../assets/logo.png" height="50" width="50"></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#1">Roles</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Candidates</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">View staff skills</a>
                    </li>
                </ul>
                <button type="button" class="btn btn-secondary">Logout</button>
            </div>
        </div>
    </nav>
    <!-- form starts here -->
    <div class="container mt-4">
        <h1>Create a new role listing</h1>
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
                    maxlength="1000" pattern="[A-Za-z\s]+"></textarea>
            </div>

            <!-- Role Requirements -->
            <div class="form-group mb-3">
                <label for="roleRequirements">Role Requirements</label>
                <textarea class="form-control" id="roleRequirements" v-model="Role_Requirements" required maxlength="1000"
                    pattern="[A-Za-z\s]+"></textarea>
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
                    <li class="mb-2" v-for="(skill, index) in selectedSkills" :key="index">
                        {{ skill }}
                        <button @click="removeSkill(index)" style="border-radius: 5px;">Remove</button>
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
        </form>
    </div>
</template>
  
  
<script>
import axios from 'axios'
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
            this.Skills = this.formattedSkills;
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
            }).then(response => console.log(response));
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

    },
    mounted() {
        axios.get('http://127.0.0.1:5000/api/skills').then(response => this.availableSkills = response.data)
    }
};
</script>
  
<style scoped>
.btn {
    margin-top: 10px;
    margin-bottom: 40px;
}
</style>