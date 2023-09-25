document.addEventListener('DOMContentLoaded', function () {
    const firstnameInput = document.getElementById('first_name');
    const lastnameInput = document.getElementById('last_name');
    const panInput = document.getElementById('pan_number');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const phoneInput = document.getElementById('phone-number');
    const pincodeInput = document.getElementById('pincode');
    const accountHolderNameInput = document.getElementById('account-holder-name');
    const accountNumberInput = document.getElementById('account-number');
    const bankNameInput = document.getElementById('bank-name');
    const branchNameInput = document.getElementById('branch');
    const ifscCodeInput = document.getElementById('ifsc-code');

    function validateFirstName() {
        const firstnameError = document.getElementById('firstnameError');
        const name = firstnameInput.value.trim();
        const namePattern = /^[a-zA-Z]+$/;
    
        if (name === '') {
            firstnameInput.classList.add('is-invalid');
            firstnameError.innerText = 'Name is required.';
        } else if (!namePattern.test(name)) {
            firstnameInput.classList.add('is-invalid');
            firstnameError.innerText = 'Name should contain only alphabets.';
        } else {
            firstnameInput.classList.remove('is-invalid');
            firstnameError.innerText = '';
        }
    }

    // Function to validate last name
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

    function validatePAN() {
        const panError = document.getElementById('panError');
        const pan = panInput.value.trim();
        const panPattern = /^([A-Z]){5}([0-9]){4}([A-Z]){1}$/;

        if (!panPattern.test(pan)) {
            panInput.classList.add('is-invalid');
            panError.innerText = 'Invalid PAN number format. Example: ABCDE1234F';
        } else {
            panInput.classList.remove('is-invalid');
            panError.innerText = '';
        }
    }

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

    function containsUppercase(text) {
        return /[A-Z]/.test(text);
      }
    
    function containsLowercase(text) {
        return /[a-z]/.test(text);
    }
    
    function containsSpecialCharacter(text) {
        return /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(text);
    }

    function containsNumber(text) {
        return /[0-9]/.test(text);
    }

    function validatePhoneNumber() {
        const phoneError = document.getElementById('phoneError');
        const phone = phoneInput.value.trim();
        const phonePattern = /^[6789]\d{9}$/;

        if (!phonePattern.test(phone)) {
            phoneInput.classList.add('is-invalid');
            phoneError.innerText = 'Invalid phone number format. Please enter a 10-digit number.';
        } else {
            phoneInput.classList.remove('is-invalid');
            phoneError.innerText = '';
        }
    }

    function validatePincode() {
        const pincodeError = document.getElementById('pincodeError');
        const pincode = pincodeInput.value.trim();
        const pincodePattern = /^[1-9][0-9]{5}$/;

        if (!pincodePattern.test(pincode)) {
            pincodeInput.classList.add('is-invalid');
            pincodeError.innerText = 'Invalid pincode format. Please enter a 6-digit pincode starting with a non-zero digit.';
        } else {
            pincodeInput.classList.remove('is-invalid');
            pincodeError.innerText = '';
        }
    }

    function validateAccountHolderName() {
        const accountHolderNameError = document.getElementById('accountHolderNameError');
        const name = accountHolderNameInput.value.trim();
        const namePattern = /^[A-Za-z ]+$/;

        if (!namePattern.test(name)) {
            accountHolderNameInput.classList.add('is-invalid');
            accountHolderNameError.innerText = 'Account holder name should contain only alphabets.';
        } else {
            accountHolderNameInput.classList.remove('is-invalid');
            accountHolderNameError.innerText = '';
        }
    }

    // Function to validate bank account number
    function validateAccountNumber() {
        const accountNumberError = document.getElementById('accountNumberError');
        const accountNumber = accountNumberInput.value.trim();
        const accountNumberPattern = /^\d{9,18}$/; // Adjust the pattern as needed

        if (!accountNumberPattern.test(accountNumber)) {
            accountNumberInput.classList.add('is-invalid');
            accountNumberError.innerText = 'Please enter a valid account number.';
        } else {
            accountNumberInput.classList.remove('is-invalid');
            accountNumberError.innerText = '';
        }
    }

    function validateBankName() {
        const bankNameError = document.getElementById('bankNameError');
        const bankName = bankNameInput.value.trim();
        const bankNamePattern = /^[a-zA-Z\s]+$/; // Allows only alphabets and spaces

        if (!bankNamePattern.test(bankName)) {
            bankNameInput.classList.add('is-invalid');
            bankNameError.innerText = 'Please enter a valid bank name.';
        } else {
            bankNameInput.classList.remove('is-invalid');
            bankNameError.innerText = '';
        }
    }

    function validateBranchName() {
        const branchNameError = document.getElementById('branchNameError');
        const branchName = branchNameInput.value.trim();
        const branchNamePattern = /^[a-zA-Z\s]+$/; // Allows only alphabets and spaces

        if (!branchNamePattern.test(branchName)) {
            branchNameInput.classList.add('is-invalid');
            branchNameError.innerText = 'Please enter a valid branch name.';
        } else {
            branchNameInput.classList.remove('is-invalid');
            branchNameError.innerText = '';
        }
    }

    function validateIFSCCode() {
        const ifscCodeError = document.getElementById('ifscCodeError');
        const ifscCode = ifscCodeInput.value.trim();
        const ifscCodePattern = /^[A-Z]{4}[0][\d]{6}$/; // Modify the pattern according to your requirements

        if (!ifscCodePattern.test(ifscCode)) {
            ifscCodeInput.classList.add('is-invalid');
            ifscCodeError.innerText = 'Please enter a valid IFSC code.';
        } else {
            ifscCodeInput.classList.remove('is-invalid');
            ifscCodeError.innerText = '';
        }
    }


    // Event listeners for instant validation
    firstnameInput.addEventListener('input', validateFirstName);
    lastnameInput.addEventListener('input', validateLastName);
    panInput.addEventListener('input', validatePAN);
    emailInput.addEventListener('input', validateEmail);
    passwordInput.addEventListener('input', validatePassword);
    confirmPasswordInput.addEventListener('input', validateConfirmPassword);
    phoneInput.addEventListener('input', validatePhoneNumber);
    pincodeInput.addEventListener('input', validatePincode);
    accountHolderNameInput.addEventListener('input', validateAccountHolderName);
    accountNumberInput.addEventListener('input', validateAccountNumber);
    bankNameInput.addEventListener('input', validateBankName);
    branchNameInput.addEventListener('input', validateBranchName);
    ifscCodeInput.addEventListener('input', validateIFSCCode);

    // Event listeners for section 1 submission
    const submitStep1Button = document.getElementById('submit_step1');
    submitStep1Button.addEventListener('click', function (event) {
        validateFirstName();
        validateLastName();
        validatePAN();
        validateEmail();
        validatePassword();
        validateConfirmPassword();

        // Check for empty fields
        if (
            firstnameInput.classList.contains('is-invalid') ||
            lastnameInput.classList.contains('is-invalid') ||
            panInput.classList.contains('is-invalid') ||
            emailInput.classList.contains('is-invalid') ||
            passwordInput.classList.contains('is-invalid') ||
            confirmPasswordInput.classList.contains('is-invalid') ||
            firstnameInput.value.trim() === '' ||
            lastnameInput.value.trim() === '' ||
            panInput.value.trim() === '' ||
            emailInput.value.trim() === '' ||
            passwordInput.value.trim() === '' ||
            confirmPasswordInput.value.trim() === ''
        ) {
            event.preventDefault(); // Prevent submission if there are errors or empty fields in section 1
        }
    });

    // Event listeners for section 2 submission
    const submitStep2Button = document.getElementById('submit_step2');
    submitStep2Button.addEventListener('click', function (event) {
        validatePhoneNumber();
        validatePincode();

        // Check for empty fields
        if (
            phoneInput.classList.contains('is-invalid') ||
            pincodeInput.classList.contains('is-invalid') ||
            isEmpty(phoneInput.value) ||
            isEmpty(pincodeInput.value)
        ) {
            event.preventDefault(); // Prevent submission if there are errors or empty fields in section 2
        }
    });

    // Event listeners for section 3 submission
    const submitStep3Button = document.getElementById('submit_step3');
    submitStep3Button.addEventListener('click', function (event) {
        validateAccountHolderName();
        validateAccountNumber();
        validateBankName();
        validateBranchName();
        validateIFSCCode();

        // Check for empty fields
        if (
            accountHolderNameInput.classList.contains('is-invalid') ||
            accountNumberInput.classList.contains('is-invalid') ||
            bankNameInput.classList.contains('is-invalid') ||
            branchNameInput.classList.contains('is-invalid') ||
            ifscCodeInput.classList.contains('is-invalid') ||
            isEmpty(accountHolderNameInput.value) ||
            isEmpty(accountNumberInput.value) ||
            isEmpty(bankNameInput.value) ||
            isEmpty(branchNameInput.value) ||
            isEmpty(ifscCodeInput.value)
        ) {
            event.preventDefault(); // Prevent submission if there are errors or empty fields in section 3
        }
    });

    // Helper function to check if a value is empty
    function isEmpty(value) {
        return value.trim() === '';
    }

});


  