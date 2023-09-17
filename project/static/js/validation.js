document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('registerForm');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirmPassword');
  const firstnameInput = document.getElementById('first_name');
  const lastnameInput = document.getElementById('last_name');

  // Function to validate email
  function validateEmail() {
    const emailError = document.getElementById('emailError');

    if (!isValidEmail(emailInput.value)) {
      emailInput.classList.add('is-invalid');
      emailError.innerText = 'Please enter a valid email address.';
    } else {
      emailInput.classList.remove('is-invalid');
      emailError.innerText = '';
    }
  }

  // Function to validate password
  function validatePassword() {
    const passwordError = document.getElementById('passwordError');
    const password = passwordInput.value;

    const errors = [];
    if (password.length < 8) {
      errors.push('Password must be at least 8 characters long.');
    }
    if (!containsUppercase(password)) {
      errors.push('Password must contain at least one uppercase letter.');
    }
    if (!containsLowercase(password)) {
      errors.push('Password must contain at least one lowercase letter.');
    }
    if (!containsSpecialCharacter(password)) {
      errors.push('Password must contain at least one special character.');
    }
    if(!containsNumber(password)) {
      errors.push('Password must contain at least one number character.');
    }

    if (errors.length > 0) {
      passwordInput.classList.add('is-invalid');
      passwordError.innerText = errors.join(' ');
    } else {
      passwordInput.classList.remove('is-invalid');
      passwordError.innerText = '';
    }

    validateConfirmPassword();
  }

  // Function to validate confirm password
  function validateConfirmPassword() {
    const confirmPasswordError = document.getElementById('confirmPasswordError');

    if (confirmPasswordInput.value !== passwordInput.value) {
      confirmPasswordInput.classList.add('is-invalid');
      confirmPasswordError.innerText = 'Passwords do not match.';
    } else {
      confirmPasswordInput.classList.remove('is-invalid');
      confirmPasswordError.innerText = '';
    }
  }

  function validateFirstName() {
    const firstnameError = document.getElementById('firstnameError');
    const name = firstnameInput.value.trim();
    const namePattern = /^[a-zA-Z]+$/;

    if (!namePattern.test(name)) {
      firstnameInput.classList.add('is-invalid');
      firstnameError.innerText = 'Name should contain only alphabets.';
    } else {
      firstnameInput.classList.remove('is-invalid');
      firstnameError.innerText = '';
    }
  }

  function validateLastName() {
    const lastnameError = document.getElementById('lastnameError');
    const name = lastnameInput.value.trim();
    const namePattern = /^[a-zA-Z ]+$/;

    if (!namePattern.test(name)) {
      lastnameInput.classList.add('is-invalid');
      lastnameError.innerText = 'Name should contain only alphabets.';
    } else {
      lastnameInput.classList.remove('is-invalid');
      lastnameError.innerText = '';
    }
  }

  // Helper functions for validation
  function containsUppercase(text) {
    return /[A-Z]/.test(text);
  }

  function containsLowercase(text) {
    return /[a-z]/.test(text);
  }

  function containsSpecialCharacter(text) {
    return /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(text);
  }

  function isValidEmail(email) {
    const validProviders = [
      "gmail", "yahoo", "outlook", "hotmail", "aol", "icloud", "protonmail", "zoho"
      // Add more valid providers
    ];
  
    const validTLDs = [
      "com", "org", "net", "edu", "gov", "mil", "co", "info", "io", "uk", "in"
      // Add more valid TLDs
    ];
  
    const emailParts = email.split("@");
    if (emailParts.length !== 2) {
      return false; // Email should have exactly one @ symbol
    }
  
    const provider = emailParts[1].split(".")[0].toLowerCase();
    const tld = emailParts[1].split(".").pop().toLowerCase();
  
    const emailRegex = /^[a-z0-9._%+-]+@[a-z.-]+$/;
  
    // Check for more than two periods following characters
    const afterTLD = emailParts[1].split(".").slice(1).join(".");
    if (afterTLD.includes("..") || afterTLD.split(".").length > 2) {
      return false;
    }
  
    return (
      emailRegex.test(email) &&
      validProviders.includes(provider) &&
      validTLDs.includes(tld)
    );
  }


  function containsNumber(text) {
    return /[0-9]/.test(text);
  }
  // Event listeners for instant validation
  emailInput.addEventListener('input', validateEmail);
  passwordInput.addEventListener('input', validatePassword);
  confirmPasswordInput.addEventListener('input', validateConfirmPassword);
  firstnameInput.addEventListener('input', validateFirstName);
  lastnameInput.addEventListener('input', validateLastName);

  // Form submit event listener for final validation before submission
  form.addEventListener('submit', function (event) {
    validateEmail();
    validatePassword();
    validateConfirmPassword();
    validateFirstName();
    validateLastName();

    if (emailInput.classList.contains('is-invalid') || passwordInput.classList.contains('is-invalid') || firstnameInput.classList.contains('is-invalid') || lastnameInput.classList.contains('is-invalid')){
      event.preventDefault();
    }
  });
});
