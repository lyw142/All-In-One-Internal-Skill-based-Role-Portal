<template>
    <!-- form starts here -->
    <div class="container">
        <div class="image-section">
            <img src="../assets/hiring-login.jpg" alt="Image" class="image" />
        </div>
        <div class="login-section">
            <div class="logo">
                <img src="../assets/logo.png" alt="Logo" class="logo" />
            </div>
            <h3>Login</h3>
            <form class="login-form" @submit.prevent="loginAttempt()">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" v-model="formData.email" class="form-control" required>
                </div>
                &nbsp;
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" v-model="formData.password" class="form-control" required>
                </div>
                <p></p>
                <button type="submit" class="btn btn-primary center-button">Sign in</button>
                &nbsp;
            </form>
            <div id="errorMessage" v-show="showError" class="color:red;">
                {{ errMsg }}
            </div>
        </div>
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
            errMsg:'',
            showError: false
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
                        this.showError = true;
                        this.errMsg = "Login failed. Check your credentials."
                    }
                })
                .catch(error => {
                    // Handle any errors, such as network issues or a non-200 status code
                    if (error.response && error.response.status === 404) {
                        // Handle a 404 Not Found error
                        this.showError = true;
                        this.errMsg = "User not found. Please check your credentials."
                    } else {
                        console.error("Error:", error);
                        this.showError = true;
                        this.errMsg = "An error occurred while trying to login."
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
                this.navigateBackOrHome(serializedUser)
            } else {
                return null; // No user session data found
            }
        },

        navigateBackOrHome(serializedUser) {
            if (window.history.length > 1) {
                // If there is a previous page, go back one step
                this.$router.go(-1);
            } else {
                // If there is no previous page, redirect to the home page
                if (serializedUser.Access_Rights == 4) {
                    this.$router.push("/hrnav");
                } else {
                    this.$router.push("/staffnav");
                }
            }
        }
    },
    mounted() {
        this.getUserSessionData();
    }
};
</script>
  
<style scoped>
.container {
  display: flex;
  height: 100vh;
}

.image-section {
  flex: 60%; /* 70% of the width */
  background-color: #f0f0f0; /* Optional background color for the image section */
  display: flex;
  justify-content: center;
  align-items: center;
}

.image {
  max-width: 100%; /* To make sure the image fits within its container */
  max-height: 100%;
}

.login-section {
  flex: 40%; /* 30% of the width */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.logo {
  /* Style for the logo image */
  background-color: black;
}

.login-form {
  /* Style for the login form */
    width:90%;
}

.center-button {
  display: block;
  margin: 0 auto;
}
</style>