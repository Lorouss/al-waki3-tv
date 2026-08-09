// Toggle the navigation menu when the menu button is clicked
document.getElementById('menu-toggle').addEventListener('click', function() {
    const navMenu = document.getElementById('nav-menu');
    navMenu.classList.toggle('show');
});

// Hide the navigation menu when any link inside it is clicked
document.querySelectorAll('#nav-menu a').forEach(link => {
    link.addEventListener('click', function() {
        const navMenu = document.getElementById('nav-menu');
        navMenu.classList.remove('show');
    });
});

// Hide the navigation menu when clicking outside of it
document.addEventListener('click', function(event) {
    const navMenu = document.getElementById('nav-menu');
    const menuToggle = document.getElementById('menu-toggle');

    // Check if the click was outside the menu and the menu button
    if (!navMenu.contains(event.target) && !menuToggle.contains(event.target)) {
        navMenu.classList.remove('show');
    }
});
