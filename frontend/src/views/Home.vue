<template>
    <div class="home">
        <h1>This will be the login page</h1>
    </div>
    <div class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="navbar-left">
            <img src="../assets/logo.png" alt="Logo" class="logo" />
            <a to="/roles" class="nav-link" style="color: white;">Roles</a>
            <a to="/candidates" class="nav-link" style="color: white;">Candidates</a>
            <a to="/view-staff-skills" class="nav-link" style="color: white;">View Staff Skills</a>
        </div>
    </div>
    <!-- form starts here -->
    <div class="container mt-4">
        <h2>Login</h2>
        <form @submit.prevent="loginAttempt()">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="formData.email" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="formData.password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'

export default {
    data() {
        return {
            formData: {
                email: '',
                password: '',
            },
        };
    },
    methods: {
        loginAttempt() {
            axios.post('http://127.0.0.1:5000/api/login', {
                Email: this.formData.email,
                Password: this.formData.password
            })
                .then(response => {
                    console.log(response);
                    if (response.data) {
                        // Handle a successful login here
                        console.log("Login successfully")
                        this.setUserSessionData(response.data)
                        if (response.data.Access_Rights == 4) {
                            this.$router.push("/hrnav");
                        } else {
                            this.$router.push("/staffnav");
                        }
                    } else {
                        // Handle cases where login is not successful
                        console.log("Login failed. Check your credentials.");
                    }
                })
                .catch(error => {
                    // Handle any errors, such as network issues or a non-200 status code
                    if (error.response && error.response.status === 404) {
                        // Handle a 404 Not Found error
                        console.log("User not found. Please check your credentials.");
                    } else {
                        console.error("Error:", error);
                        console.log("An error occurred while trying to login.");
                    }
                });
        },
        // Set user session data in a cookie
        setUserSessionData(user) {
            // Serialize user data (e.g., user ID or authentication token)
            const serializedUser = JSON.stringify(user);

            // Set the serialized user data in a cookie with an expiration time
            Cookies.set('userSession', serializedUser, { expires: 1 }); // Example expiration time of 1 day
        },

        // Retrieve user session data from a cookie
        getUserSessionData() {
            const serializedUser = Cookies.get('userSession');

            if (serializedUser) {
                console.log(JSON.parse(serializedUser));
                // Deserialize user data from the cookie
                if (serializedUser.Access_Rights == 4) {
                    this.$router.push("/hrnav");
                } else {
                    this.$router.push("/staffnav");
                }
            } else {
                return null; // No user session data found
            }
        },
    },
    mounted() {
        this.getUserSessionData();
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

.btn {
    margin-top: 10px;
    margin-bottom: 40px;
}
</style>