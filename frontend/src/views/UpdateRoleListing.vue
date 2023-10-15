<template>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="navbar-left">
            <img src="../assets/logo.png" alt="Logo" class="logo" />
            <a to="/roles" class="nav-link" style="color: white;">Roles</a>
            <a to="/candidates" class="nav-link" style="color: white;">Candidates</a>
            <a to="/view-staff-skills" class="nav-link" style="color: white;">View Staff Skills</a>
        </div>
        <div class="navbar-right">
            <button class="btn btn-secondary">Logout</button>
        </div>
    </div>
    <!-- form starts here -->
    <div class="container mt-4">
        <h1>Update role listing</h1>
        <form @submit.prevent="submitForm">

            <!-- Role Responsibilities -->
            <div class="form-group mb-3">
                <label for="roleResponsibilities">Role Responsibilities</label>
                <textarea class="form-control" id="roleResponsibilities" v-model="this.Role_Responsibilities" required
                    maxlength="1000" pattern="[A-Za-z\s]+" rows="7"></textarea>
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
                        <li class="mb-2" v-for="skill in selectedSkills" :key="skill">
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
                    <input type="text" class="form-control" id="country" v-model="this.Country" required maxlength="20"
                        pattern="[A-Za-z\s]+" />
                </div>
            </div>


            <!-- Salary -->
            <div class="form-group mb-3">
                <div class="row">
                    <div class="col-6">
                        <label for="minSalary">Salary ($)</label>
                        <input type="number" class="form-control" id="roleSalary"
                            @input="Salary = $event.target.value.toString()" v-model="this.Salary" required
                            pattern="[0-9]{1,11}" />
                    </div>
                    <div class="form-group mb-3 col-6">
                        <label for="roleDeadline">Deadline</label>
                        <input type="date" class="form-control" id="roleDeadline" v-model="this.Deadline" required />
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-secondary">Update</button>
        </form>
    </div>
</template>
  
  
<script>
import axios from 'axios'
export default {
    props: ['Listing_ID'],
    data() {
        return {
            // variables that i used 
            selectedSkill: '',
            selectedSkills: [],
            availableSkills: [],
            originalSkills: [],
            addedSkills: [],
            removedSkills: [],
            addedSkills_ID: [],
            removedSkills_ID: [],

            Role_Responsibilities: "",
            Salary: "",
            Skills: [],
            Deadline: "",
            Country: "",



        };
    },
    methods: {
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
            axios.post(url, {
                Role_Responsibilities: this.Role_Responsibilities,
                Salary: this.Salary,
                AddedSkills: this.addedSkills_ID,
                RemovedSkills: this.removedSkills_ID,
                Deadline: this.Deadline,
                Country: this.Country,
            }).then(response => {
                console.log(response);
                alert("The role listing has been updated");
                this.$router.push("/hrnav");
            });

            // console.log({
            //     Role_Responsibilities: this.Role_Responsibilities,
            //     Salary: this.Salary,
            //     Deadline: this.Deadline,
            //     Country: this.Country,
            // })

        }

    },
    mounted() {
        const apiUrl = `http://127.0.0.1:5000/api/getRoleListing/${this.Listing_ID}`;
        axios.get(apiUrl).then(response => {
            this.Role_Responsibilities = response.data[0].Role_Responsibilities;
            this.Salary = response.data[0].Salary;
            this.Deadline = response.data[0].Deadline;
            this.Country = response.data[0].Country;
            this.selectedSkills = response.data[0].Skills;
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
.btn {
    margin-top: 10px;
    margin-bottom: 40px;
}

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
</style>