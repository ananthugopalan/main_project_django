$(document).ready(function () {
    $('#register_form').submit(function (event) {
        if (!validateForm()) {
            event.preventDefault();
        }
    });

    function validateForm() {
        let isValid = true;
        const profilePhoto = $('#profilePhoto');
        const firstName = $('#first_name');
        const lastName = $('#last_name');
        const gender = $('#gender');
        const email = $('#email').val().trim();
        // Add other fields here...

        if (!profilePhoto.val()) {
            isValid = false;
            $('#profilePhotoError').show();
        } else {
            const fileExtension = profilePhoto.val().split('.').pop().toLowerCase();
            if ($.inArray(fileExtension, ['png', 'jpg', 'jpeg']) === -1) {
                isValid = false;
                $('#profilePhotoError').show();
            }
        }

        if (!/^[a-zA-Z]+$/.test(firstName.val().trim())) {
            isValid = false;
            $('#first_name_error').show();
        }

        if (!/^[a-zA-Z]+$/.test(lastName.val().trim())) {
            isValid = false;
            $('#last_name_error').show();
        }

        if (!gender.val()) {
            isValid = false;
            $('#gender_error').show();
        }

        if (!email || !validateEmail(email)) {
            isValid = false;
            $('#emailError').text('Please enter a valid email address.');
            $('#emailError').show();
        } else {
            $('#emailError').hide();
        }

        // Add validation for other fields...

        return isValid;
    }
    function validateEmail(email) {
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
});