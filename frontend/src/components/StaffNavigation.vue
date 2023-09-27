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
          <div v-for="(role, index) in roles" :key="index">
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">{{ role.title }}</h5>
                <p class="card-text">
                  <strong>Skills Required:</strong>
                  <span v-for="(skill, index) in role.skills.split(',')" :key="index" class="skill-box">
                    {{ skill.trim() }}
                  </span>
                </p>
                <ul>
                  <li v-for="(line, index) in role.description.split('\n')" :key="index">
                    {{ line }}
                  </li>
                </ul>
                <p class="card-text">
                  <strong>Application Deadline:</strong> Closed in
                  {{ role.deadline }} days
                </p>
              </div>
            </div>
          </div>
        </div>
        <div :style="{ width: '60%', marginLeft: '16px' }">
          <div class="card">
            <div>
              <div class="divider">
                <h3 class="card-title">{{ selectedRole.title }}</h3>
                <p>$2000-$2500 a month, Full time</p>
              </div>
              <div class="divider">
                <h3 class="card-title">Role description</h3>
                <div class="role-description">
                  <strong>Job responsabilities</strong>
                  <ol>
                    <li>
                      Bachelor's degree in Human Resources, Business
                      Administration, or a related field (or equivalent
                      experience).
                    </li>
                    <li>
                      Strong communication skills, both written and verbal.
                    </li>
                    <li>Basic understanding of HR policies and procedures.</li>
                    <!-- Add more description items as needed -->
                  </ol>
                </div>

                <!-- Role Requirements -->
                <div class="role-requirements">
                  <strong>Role Requirements</strong>
                  <ol>
                    <li>
                      Bachelor's degree in Human Resources, Business
                      Administration, or a related field (or equivalent
                      experience).
                    </li>
                    <li>
                      Strong communication skills, both written and verbal.
                    </li>
                    <li>Basic understanding of HR policies and procedures.</li>
                    <!-- Add more requirements as needed -->
                  </ol>
                </div>
              </div>
              <div class="skills">
                <p>
                  <strong>Skills Required:</strong>
                </p>
                <span v-for="(skill, index) in selectedRole.skills.split(',')" :key="index" class="skill-box">
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
export default {
  data() {
    return {
      openCount: 0,
      closedCount: 0,
      searchQuery: "",
      roles: [
        {
          title: "Human Resource (Entry Level)",
          skills: "Communication, Recruitment, HR Policies",
          description:
            "We are seeking an Entry Level Human Resource professional to join our team. This role involves assisting with recruitment, onboarding, and HR policy compliance.\n Ideal candidates should have strong communication skills and a desire to grow in the field of HR.",
          deadline: 7, // Number of days until the application deadline
        },
        {
          title: "Human Resource Officer",
          skills: "Employee Relations, Benefits Administration, HR Compliance",
          description:
            "We are looking for an experienced Human Resource Officer to manage HR functions, including employee relations, benefits administration, and ensuring HR compliance.\n The ideal candidate should have a strong background in HR and excellent problem-solving skills.",
          deadline: 14, // Number of days until the application deadline
        },
        {
          title: "Real Estate Sale Coordinator",
          skills: "Real Estate Sales, Customer Service, Negotiation",
          description:
            "Join our real estate team as a Sale Coordinator!\n This role involves coordinating real estate transactions, providing excellent customer service to clients, and assisting with negotiations.\n If you have a passion for real estate and a customer-centric approach, we want to hear from you.",
          deadline: 5, // Number of days until the application deadline
        },
        // Add more role objects as needed
      ],
      selectedRole: {
        title: "Human Resource (Entry Level)",
        skills: "Communication, Recruitment, HR Policies",
        description:
          "We are seeking an Entry Level Human Resource professional to join our team. This role involves assisting with recruitment, onboarding, and HR policy compliance.\n Ideal candidates should have strong communication skills and a desire to grow in the field of HR.",
        deadline: 7, // Number of days until the application deadline
      },
    };
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
