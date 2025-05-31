// Dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    const dropdownButton = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownButton.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownContent.classList.toggle('show');
    });

    window.addEventListener('click', function(e) {
        if (!dropdownButton.contains(e.target) && !dropdownContent.contains(e.target)) {
            dropdownContent.classList.remove('show');
        }
    });

    // Animation trigger for priority box when in view
    const priorityBox = document.querySelector('.priority-box');
    window.addEventListener('scroll', () => {
        const boxPosition = priorityBox.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        if (boxPosition < screenPosition) {
            priorityBox.style.opacity = 1;
        }
    });
});
