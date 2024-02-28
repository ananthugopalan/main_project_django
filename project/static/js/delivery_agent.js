document.getElementById('register_form').addEventListener('submit', function(event) {
    event.preventDefault();

    if (validateForm()) {
        this.submit();
    } else {
        alert('Please correct the errors in the form before submitting.');
    }
});

function validateForm() {
    let isValid = true;

    isValid = isValid && validateProfilePhoto();
    isValid = isValid && validateFirstName();
    isValid = isValid && validateLastName();
    isValid = isValid && validateGender();
    isValid = isValid && validateEmail();
    isValid = isValid && validatePassword();
    isValid = isValid && validateConfirmPassword();
    isValid = isValid && validatePhoneNumber();
    isValid = isValid && validateAddress();
    isValid = isValid && validateLocation();
    isValid = isValid && validateAadhaarNumber();
    isValid = isValid && validateDriverLicenseNumber();
    isValid = isValid && validateDateOfJoining();
    isValid = isValid && validateVehicleType();
    isValid = isValid && validateVehicleNumber();
    isValid = isValid && validateBankName();
    isValid = isValid && validateBranch();
    isValid = isValid && validateAccountNumber();
    isValid = isValid && validateIFSCCode();

    return isValid;
}

function validateProfilePhoto() {
    const fileInput = document.getElementById('profilePhoto');
    const file = fileInput.files[0];
    const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

    if (!allowedExtensions.exec(file.name)) {
        document.getElementById('fileError').style.display = 'block';
        fileInput.value = '';
        return false;
    } else {
        document.getElementById('fileError').style.display = 'none';
        return true;
    }
}

function validateFirstName() {
    const firstNameInput = document.getElementById('first_name');
    const firstName = firstNameInput.value.trim();
    const containsOnlyAlphabets = /^[A-Za-z]+$/.test(firstName);

    if (!containsOnlyAlphabets) {
        document.getElementById('firstNameError').style.display = 'block';
        return false;
    } else {
        document.getElementById('firstNameError').style.display = 'none';
        return true;
    }
}

function validateLastName() {
    const lastNameInput = document.getElementById('last_name');
    const lastName = lastNameInput.value.trim();
    const containsOnlyAlphabets = /^[A-Za-z\s]+$/.test(lastName);

    if (!containsOnlyAlphabets) {
        document.getElementById('lastNameError').style.display = 'block';
        return false;
    } else {
        document.getElementById('lastNameError').style.display = 'none';
        return true;
    }
}

function validateGender() {
    const genderInput = document.getElementById('gender');

    if (genderInput.value === '') {
        document.getElementById('genderError').style.display = 'block';
        return false;
    } else {
        document.getElementById('genderError').style.display = 'none';
        return true;
    }
}

function validateEmail() {
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const email = emailInput.value.trim();
    const validProviders = ["gmail", "yahoo", "outlook", "hotmail", "aol", "icloud", "protonmail", "zoho"];
    const validTLDs = ["com", "org", "net", "edu", "gov", "mil", "co", "info", "io", "uk", "in"];
    const emailParts = email.split("@");
    if (emailParts.length !== 2) {
        emailInput.classList.add('is-invalid');
        emailError.innerText = 'Please enter a valid email address.';
        emailError.style.display = 'block';
        return false;
    }
    const provider = emailParts[1].split(".")[0].toLowerCase();
    const tld = emailParts[1].split(".").pop().toLowerCase();
    const emailRegex = /^[a-z0-9._%+-]+@[a-z.-]+$/;
    const afterTLD = emailParts[1].split(".").slice(1).join(".");
    if (afterTLD.includes("..") || afterTLD.split(".").length > 2) {
        emailInput.classList.add('is-invalid');
        emailError.innerText = 'Please enter a valid email address.';
        emailError.style.display = 'block';
        return false;
    }
    if (
        !emailRegex.test(email) ||
        !validProviders.includes(provider) ||
        !validTLDs.includes(tld)
    ) {
        emailInput.classList.add('is-invalid');
        emailError.innerText = 'Please enter a valid email address with a supported provider and TLD.';
        emailError.style.display = 'block';
        return false;
    } else {
        emailInput.classList.remove('is-invalid');
        emailError.innerText = '';
        emailError.style.display = 'none';
        return true;
    }
}

function validatePassword() {
    var passwordInput = document.getElementById('password');
    var password = passwordInput.value;

    var passwordError = document.getElementById('passwordError');
    var valid = true;

    if (!/[A-Z]/.test(password)) {
        valid = false;
    }
    if (!/[a-z]/.test(password)) {
        valid = false;
    }
    if (!/[0-9]/.test(password)) {
        valid = false;
    }
    if (!/[^A-Za-z0-9]/.test(password)) {
        valid = false;
    }
    if (password.length < 6) {
        valid = false;
    }
    if (valid) {
        passwordError.style.display = 'none';
        return true;
    } else {
        passwordError.style.display = 'block';
        return false;
    }
}

function validateConfirmPassword() {
    var confirmPasswordInput = document.getElementById('confirmPassword');
    var confirmPassword = confirmPasswordInput.value;
    var passwordInput = document.getElementById('password');
    var password = passwordInput.value;

    var confirmPasswordError = document.getElementById('confirmPasswordError');

    if (confirmPassword === password) {
        confirmPasswordError.style.display = 'none';
        return true;
    } else {
        confirmPasswordError.style.display = 'block';
        return false;
    }
}

function validatePhoneNumber() {
    const phoneInput = document.getElementById('phone');
    const phoneError = document.getElementById('phoneError');
    const phoneNumber = phoneInput.value.trim();
    const phoneRegex = /^[6-9]\d{9}$/;

    if (!phoneRegex.test(phoneNumber)) {
        phoneInput.classList.add('is-invalid');
        phoneError.innerText = 'Please enter a valid 10-digit phone number starting with 6, 7, 8, or 9.';
        phoneError.style.display = 'block';
        return false;
    } else {
        phoneInput.classList.remove('is-invalid');
        phoneError.innerText = '';
        phoneError.style.display = 'none';
        return true;
    }
}

function validateAddress() {
    // Validation logic for address field goes here
    const addressInput = document.getElementById('address');

    if (addressInput.value === '') {
        document.getElementById('addressError').style.display = 'block';
        return false;
    } else {
        document.getElementById('addressError').style.display = 'none';
        return true;
    }
}

function validateLocation() {
    // Validation logic for location field goes here
    const locationInput = document.getElementById('location');

    if (locationInput.value === '') {
        document.getElementById('locationError').style.display = 'block';
        return false;
    } else {
        document.getElementById('locationError').style.display = 'none';
        return true;
    }
}

function validateAadhaarNumber() {
    // Get the Aadhaar number value
    const aadhaarInput = document.getElementById('id_number');
    const aadhaarError = document.getElementById('aadhaarError');
    const aadhaarNumber = aadhaarInput.value;

    // Regular expression to validate Aadhaar number format (exactly 12 digits, not starting with 0)
    const aadhaarRegex = /^[1-9]\d{11}$/;

    // Check if the Aadhaar number is valid
    if (!aadhaarRegex.test(aadhaarNumber)) {
        // Show error message and add 'is-invalid' class
        aadhaarInput.classList.add('is-invalid');
        aadhaarError.innerText = 'Please enter a valid Aadhaar number containing exactly 12 digits and not starting with 0.';
        aadhaarError.style.display = 'block';
    } else {
        // Remove error message and 'is-invalid' class
        aadhaarInput.classList.remove('is-invalid');
        aadhaarError.innerText = '';
        aadhaarError.style.display = 'none';
    }

    return true;
}


function validateVehicleNumber() {
    // Validation logic for vehicle number field goes here
    const allowedStateCodes = ['AP', 'AR', 'AS', 'BR', 'CG', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OR', 'PB', 'RJ', 'SK', 'TN', 'TR', 'UK', 'UP', 'WB'];

    // Get the Vehicle Number input element and error message element
    const vehicleInput = document.getElementById('vehicle_number');
    const vehicleError = document.getElementById('vehicleError');
    const vehicleNumber = vehicleInput.value.toUpperCase();

        // Check if the first two characters (state code) are in the allowed state codes
        const stateCode = vehicleNumber.substring(0, 2);
        if (!allowedStateCodes.includes(stateCode)) {
            // Show error message and add 'is-invalid' class
            vehicleInput.classList.add('is-invalid');
            vehicleError.innerText = 'Please enter a valid Vehicle Number with a valid state code.';
            vehicleError.style.display = 'block';
        } else {
            // Remove error message and 'is-invalid' class
            vehicleInput.classList.remove('is-invalid');
            vehicleError.innerText = '';
            vehicleError.style.display = 'none';
        }
    
    return true;
}

function validateDriverLicenseNumber() {
    // Validation logic for driver license number field goes here
    const licenseInput = document.getElementById('driver_license_number');
    const licenseError = document.getElementById('licenseError');
    const licenseNumber = licenseInput.value;

        // Regular expression to validate Kerala Driver License Number format
        // Format: KL-XX-YYYY-NNNNNN (X: Letter, Y: Digit)
        const licenseRegex = /^KL-[A-Z]{2}-\d{4}-\d{6}$/;

        // Check if the Driver License Number is valid
        if (!licenseRegex.test(licenseNumber)) {
            // Show error message and add 'is-invalid' class
            licenseInput.classList.add('is-invalid');
            licenseError.innerText = 'Please enter a valid Kerala Driver License Number in the format KL-XX-YYYY-NNNNNN.';
            licenseError.style.display = 'block';
        } else {
            // Remove error message and 'is-invalid' class
            licenseInput.classList.remove('is-invalid');
            licenseError.innerText = '';
            licenseError.style.display = 'none';
        }
    return true;
}

function validateBankName() {
    // Validation logic for bank name field goes here
    const bankInput = document.getElementById('bank_name');

    if (bankInput.value === '') {
        document.getElementById('bankError').style.display = 'block';
        return false;
    } else {
        document.getElementById('bankError').style.display = 'none';
        return true;
    }
}

function validateBranch() {
    const branchInput = document.getElementById('branch');
    const branchError = document.getElementById('branchError');
    const regex = /^[a-zA-Z]+$/;

    if (!regex.test(branchInput.value)) {
        branchInput.classList.add('is-invalid');
        branchError.innerText = 'Branch name should contain only alphabets without spaces.';
        branchError.style.display = 'block';
        return false;
    } else {
        branchInput.classList.remove('is-invalid');
        branchError.innerText = '';
        branchError.style.display = 'none';
        return true;
    }
}

function validateAccountNumber() {
    const accountNumberInput = document.getElementById('account_number');
    const accountNumberError = document.getElementById('accountNumberError');
    const accountNumber = accountNumberInput.value.trim();

    if (!/^\d{9,18}$/.test(accountNumber)) {
        accountNumberInput.classList.add('is-invalid');
        accountNumberError.innerText = 'Account number must contain 9 to 18 digits.';
        accountNumberError.style.display = 'block';
        return false;
    } else {
        accountNumberInput.classList.remove('is-invalid');
        accountNumberError.innerText = '';
        accountNumberError.style.display = 'none';
        return true;
    }
}

function validateIFSCCode() {
    const ifscCodeInput = document.getElementById('ifsc_code');
    const ifscCodeError = document.getElementById('ifscCodeError');
    const ifscCode = ifscCodeInput.value.trim();
    const ifscRegex = /^[A-Z]{4}[0][A-Z0-9]{6}$/;

    if (!ifscRegex.test(ifscCode)) {
        ifscCodeInput.classList.add('is-invalid');
        ifscCodeError.innerText = 'IFSC code should be in the format XXXX0000XXX.';
        ifscCodeError.style.display = 'block';
        return false;
    } else {
        ifscCodeInput.classList.remove('is-invalid');
        ifscCodeError.innerText = '';
        ifscCodeError.style.display = 'none';
        return true;
    }
}
