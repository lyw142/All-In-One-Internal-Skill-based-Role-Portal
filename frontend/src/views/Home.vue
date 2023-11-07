<template>
    <!-- form starts here -->
    <!-- <div class="container">
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
    </div> -->
    <section class="vh-100">
        <div class="container-fluid h-custom">
            <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col-md-9 col-lg-6 col-xl-5">
                    <img src="../assets/login.png" class="img-fluid" alt="Login image">
                </div>
                <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
                    <h2 class="form-title">Log in</h2>
                    <form @submit.prevent="loginAttempt()">
                        <!-- Email input -->
                        <div class="form-outline mb-4">
                            <label class="form-label" for="email">Email address</label>
                            <input type="email" id="email" class="form-control form-control-lg" v-model="formData.email"
                                required />
                        </div>
                        <!-- Password input -->
                        <div class="form-outline mb-3">
                            <label class="form-label" for="password">Password</label>
                            <input type="password" id="password" class="form-control form-control-lg"
                                v-model="formData.password" required />
                        </div>
                        <div class="text-center text-lg-start pt-2">
                            <button type="submit" class="btn btn-secondary btn-lg"
                                style="padding-left: 2.5rem; padding-right: 2.5rem;">Login</button>
                        </div>
                        <div id="errorMessage" v-show="showError" class="color:red;">
                            {{ errMsg }}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
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
            errMsg: '',
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
.divider:after,
.divider:before {
    content: "";
    flex: 1;
    height: 1px;
    background: #eee;
}

.h-custom {
    height: calc(100% - 73px);
}

@media (max-width: 450px) {
    .h-custom {
        height: 100%;
    }
}

h2 {
    line-height: 1.66;
    margin: 0;
    padding: 0;
    font-weight: 700;
    color: #222;
    font-size: 36px;
}
</style>