// Import the js-cookie library
import Cookies from 'js-cookie';

// Set user session data in a cookie
function setUserSessionData(user) {
  // Serialize user data (e.g., user ID or authentication token)
  const serializedUser = JSON.stringify(user);
  
  // Set the serialized user data in a cookie with an expiration time
  Cookies.set('userSession', serializedUser, { expires: 1 }); // Example expiration time of 1 day
}

// Retrieve user session data from a cookie
function getUserSessionData() {
    const serializedUser = Cookies.get('userSession');
    
    if (serializedUser) {
      // Deserialize user data from the cookie
      return JSON.parse(serializedUser);
    } else {
      return null; // No user session data found
    }
  }

  // Clear user session data from the cookie
function clearUserSessionData() {
    Cookies.remove('userSession');
}

  

