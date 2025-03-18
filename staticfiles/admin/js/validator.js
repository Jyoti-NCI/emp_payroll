document.addEventListener("DOMContentLoaded", function () {
    let registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            if (!validateForm(registerForm)) {
                event.preventDefault(); // Prevent form submission if validation fails
            }
        });
    }

    // Attach event listeners for real-time validation
    let inputs = document.querySelectorAll("input[required], input[pattern]");
    inputs.forEach((input) => {
        input.addEventListener("input", function () {
            validateField(input);
        });
    });
});

// Function to validate individual fields
function validateField(input) {
    let errorElement = document.getElementById(input.id + "Error");
    
    if (!errorElement) {
        errorElement = document.createElement("small");
        errorElement.id = input.id + "Error";
        errorElement.className = "text-danger";
        input.parentNode.appendChild(errorElement);
    }

    if (!input.checkValidity()) {
        errorElement.innerText = input.validationMessage || input.title;
    } else {
        errorElement.innerText = "";
    }
}

// Function to validate email format
function validateEmail(input) {
    let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    let errorElement = document.getElementById(input.id + "Error");

    if (!emailPattern.test(input.value)) {
        errorElement.innerText = "Please enter a valid email address.";
        input.setCustomValidity("Invalid email format");
    } else {
        errorElement.innerText = "";
        input.setCustomValidity("");
    }
}

// Function to validate Date of Birth (must be at least 22 years old)
function validateDOB(input) {
    let dob = new Date(input.value);
    let today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    let monthDiff = today.getMonth() - dob.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
        age--;
    }

    let errorElement = document.getElementById(input.id + "Error");

    if (age < 22) {
        errorElement.innerText = "Employee must be at least 22 years old.";
        input.setCustomValidity("Invalid age");
    } else {
        errorElement.innerText = "";
        input.setCustomValidity("");
    }
}

// Function to validate password strength
function validatePassword(input) {
    let passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    let errorElement = document.getElementById(input.id + "Error");

    if (!passwordPattern.test(input.value)) {
        errorElement.innerText = "Password must be at least 8 characters long and include uppercase, lowercase, a number, and a special character.";
        input.setCustomValidity("Invalid password format");
    } else {
        errorElement.innerText = "";
        input.setCustomValidity("");
    }
}

// Function to validate password confirmation
function validatePasswordMatch(passwordInput, confirmPasswordInput) {
    let errorElement = document.getElementById(confirmPasswordInput.id + "Error");

    if (passwordInput.value !== confirmPasswordInput.value) {
        errorElement.innerText = "Passwords do not match.";
        confirmPasswordInput.setCustomValidity("Passwords do not match");
    } else {
        errorElement.innerText = "";
        confirmPasswordInput.setCustomValidity("");
    }
}

// Function to validate form before submission
function validateForm(form) {
    let isValid = true;
    let inputs = form.querySelectorAll("input[required], input[pattern]");

    inputs.forEach((input) => {
        validateField(input);
        if (!input.checkValidity()) {
            isValid = false;
        }
    });

    let emailInput = form.querySelector("input[type='email']");
    if (emailInput) validateEmail(emailInput);

    let dobInput = form.querySelector("input[type='date']");
    if (dobInput) validateDOB(dobInput);

    let passwordInput = form.querySelector("input[name='password1']");
    let confirmPasswordInput = form.querySelector("input[name='password2']");

    if (passwordInput && confirmPasswordInput) {
        validatePassword(passwordInput);
        validatePasswordMatch(passwordInput, confirmPasswordInput);
    }

    return isValid;
}

// Function to calculate total salary dynamically
function calculateSalary() {
    let baseSalaryInput = document.getElementById("baseSalary");
    let bonusInput = document.getElementById("bonus");
    let deductionsInput = document.getElementById("deductions");
    let salaryInput = document.getElementById("employeesalary");

    if (!baseSalaryInput || !bonusInput || !deductionsInput || !salaryInput) {
        console.error("One or more salary input fields are missing.");
        return;
    }

    let baseSalary = parseFloat(baseSalaryInput.value) || 0;
    let bonus = parseFloat(bonusInput.value) || 0;
    let deductions = parseFloat(deductionsInput.value) || 0;

    let totalSalary = baseSalary + bonus - deductions;

    console.log("Base Salary:", baseSalary);
    console.log("Bonus:", bonus);
    console.log("Deductions:", deductions);
    console.log("Total Salary:", totalSalary);

    salaryInput.value = totalSalary.toFixed(2);
}

