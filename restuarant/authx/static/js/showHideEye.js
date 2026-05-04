document.querySelectorAll(".showHideEye").forEach(eye => {
    eye.addEventListener("click", () => {
        const input = eye.previousElementSibling;
        const icon = eye.querySelector("i");

        if (input.type === "password") {
            input.type = "text";
            icon.classList.replace("fa-eye-slash", "fa-eye");
        } else {
            input.type = "password";
            icon.classList.replace("fa-eye", "fa-eye-slash");
        }
    });
});