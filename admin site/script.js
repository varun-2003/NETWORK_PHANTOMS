// Your Firebase configuration
const firebaseConfig = {
  // space for firebase credentials
};

firebase.initializeApp(firebaseConfig);

// Check authentication state on page load
firebase.auth().onAuthStateChanged(user => {
  if (!user) {
    // User is not signed in, redirect to login page
    window.location.href = 'index.html';
  } else {
    console.log('User is signed in:', user);
  }
});

// Logout function
document.getElementById('logoutBtn').addEventListener('click', () => {
  firebase.auth().signOut().then(() => {
    console.log('User signed out successfully.');
    alert('Logged out successfully.');
    window.location.href = 'index.html';
  }).catch(error => {
    console.error('Error logging out:', error);
    alert('Error logging out: ' + error.message);
  });
});

// Scroll function
function scrollToElement(elementSelector, instance = 0) {
  const elements = document.querySelectorAll(elementSelector);
  if (elements.length > instance) {
    elements[instance].scrollIntoView({ behavior: 'smooth' });
  }
}

const link1 = document.getElementById("link1");
const link2 = document.getElementById("link2");
const link3 = document.getElementById("link3");

link1.addEventListener('click', () => {
  scrollToElement('.header');
});

link2.addEventListener('click', () => {
  scrollToElement('.header', 1);
});

link3.addEventListener('click', () => {
  scrollToElement('.column');
});
