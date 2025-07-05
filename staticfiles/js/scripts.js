// Example custom JavaScript code

document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom scripts loaded.');

    // Example: Add event listener to a button
    const myButton = document.getElementById('myButton');
    if (myButton) {
        myButton.addEventListener('click', function() {
            alert('Button clicked!');
        });
    }
});