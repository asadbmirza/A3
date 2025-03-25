const usernameField = document.querySelector('#username');
const passwordField = document.querySelector('#password');
const fnameField = document.querySelector('#fname');
const lnameField = document.querySelector('#lname');
const accountTypeField = document.querySelector('#accountType');
const submitButton = document.querySelector('.authenticateButton');
const form = document.querySelector('.authenticateForm');


const createErrorMessage = (field, message) => {
    removeErrorMessage(field);

    const errorElement = document.createElement('span');
    errorElement.classList.add('flash'); 
    errorElement.classList.add('error'); 
    errorElement.textContent = message;

    field.insertAdjacentElement('afterend', errorElement);
}
const removeErrorMessage = (field) => {
    const existingError = field.nextElementSibling;

    if (existingError && existingError.classList.contains('error')) {
        existingError.remove();
    }
}

const validateCommon = () => {
    let error = false;
    if (!usernameField.value) {
        createErrorMessage(usernameField, 'Username is required.');
        error = true;
    } else {
        removeErrorMessage(usernameField); 
    }
    
    if (!passwordField.value) {
        createErrorMessage(passwordField, 'Password is required.');
        error = true;
    } else {
        removeErrorMessage(passwordField);
    }

    return error;
}

const validateRegister = () => {
    let error = false;
    if (!fnameField || !lnameField) {
        return false;
    }

    if (!fnameField.value) {
        createErrorMessage(fnameField, 'First name is required.');
        error = true;
    } else {
        removeErrorMessage(fnameField);
    }
    
    if (!lnameField.value) {
        createErrorMessage(lnameField, 'Last name is required.');
        error = true;
    } else {
        removeErrorMessage(lnameField);
    }

    return error
}


form.addEventListener("submit", (event) => {
    event.preventDefault();
    const commonError = validateCommon();
    const registerError = validateRegister();

    if (commonError || registerError) {
        return;
    }
    form.submit();
})