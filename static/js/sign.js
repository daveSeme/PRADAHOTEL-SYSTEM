// select the form and add a submit event listener
const signupForm = document.getElementById("signup-form");
signupForm.addEventListener("submit", handleFormSubmit);

function handleFormSubmit(event) {
  event.preventDefault(); // prevent the form from submitting

  // get form input values
  const name = document.getElementById("name").value;
  const id_number = document.getElementById("id_number").value;
  const gender = document.getElementById("gender").value;
  const password = document.getElementById("password").value;
  const confirm_password = document.getElementById("confirm_password").value;
  const credit_card = document.getElementById("credit_card").value;

  // validate form inputs
  if (name === "" || id_number === "" || gender === "" || password === "" || confirm_password === "" || credit_card === "") {
    alert("Please fill in all fields.");
    return;
  }

  if (password !== confirm_password) {
    alert("Passwords do not match.");
    return;
  }

  // if form is valid, send data to server
  const formData = new FormData();
  formData.append("name", name);
  formData.append("id_number", id_number);
  formData.append("gender", gender);
  formData.append("password", password);
  formData.append("credit_card", credit_card);

  fetch("http://localhost:8000/signup", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    alert("Sign up successful!");
  })
  .catch(error => {
    console.error(error);
    alert("Sign up failed. Please try again.");
  });
}
//To validate credit card number

function validateCreditCard(creditCardNumber) {
  // remove any non-digit characters from the input
  creditCardNumber = creditCardNumber.replace(/\D/g, '');

  // check that the input is a valid credit card number
  if (/[^0-9-\s]+/.test(creditCardNumber)) return false;

  // the Luhn algorithm to validate the credit card number
  let sum = 0;
  let doubleUp = false;
  for (let i = creditCardNumber.length - 1; i >= 0; i--) {
    let digit = parseInt(creditCardNumber.charAt(i));

    if (doubleUp) {
      if ((digit *= 2) > 9) digit -= 9;
    }

    sum += digit;
    doubleUp = !doubleUp;
  }

  return sum % 10 == 0;
}

// Example usage:
let creditCardInput = document.getElementById('credit-card-input').value;
if (validateCreditCard(creditCardInput)) {
  // the input is a valid credit card number
} else {
  // the input is not a valid credit card number
}

