function sendMail(contactForm) {
    emailjs.send("gmail", "ms3", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "project_request": contactForm.comments.value
    })
    .then(
        function() {
            document.getElementById("contact-form").reset();
            $('.email-response').html("Thank you for your email, someone will be in touch shortly.");
        },
        function() {
            document.getElementById("contact-form").reset();
            $('.email-response').html("There was an error with our email service. Please try again in a few minutes.");
        }
    );
    return false;
}