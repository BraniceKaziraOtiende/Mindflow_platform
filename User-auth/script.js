document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    // Basic form validation
    if (!email || !password) {
        alert("Please fill out both fields.");
        return;
    }

    // Send the data to the back-end via Fetch API
    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect or show success message
            window.location.href = "/dashboard";  // Replace with your actual route
        } else {
            // Display error message from backend
            alert(data.message);  // Show backend error message
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again later.");
    });
});
