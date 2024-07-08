document.addEventListener('DOMContentLoaded', function () {
    // Get the file input and uploaded image elements
    const fileInput = document.getElementById('imageUpload');
    const uploadedImage = document.getElementById('uploadedImage');

    // Handle file input change event
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];  // Get the selected file

        if (file) {
            const reader = new FileReader();  // Create a FileReader instance
            reader.onload = function(e) {
                uploadedImage.src = e.target.result;  // Set the src of the image to the file data URL
                uploadedImage.style.display = 'block';  // Show the uploaded image
            };
            reader.readAsDataURL(file);  // Read the file as a data URL
        }
    });

    // You can add more JavaScript code here if needed
});