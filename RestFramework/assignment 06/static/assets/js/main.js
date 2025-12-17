const Humberger = document.querySelector('.navBar .navList .humberger');
const MobileMenu = document.querySelector('.navBar .navList ul');

Humberger.addEventListener('click', () => {
    Humberger.classList.toggle('active')
    MobileMenu.classList.toggle('active')
})

document.addEventListener('scroll', () => {
    var scroll_pos = window.scrollY;
    if (scroll_pos > 250) {
        header.style.backgroundColor = "rgb(54, 217, 182)"
        header.style.boxShadow = "1px 2px 5px 0px rgb(34, 165, 137)"
    }
    else {
        header.style.backgroundColor = "rgb(54, 217, 182)"
        header.style.backgroundColor = "linear-gradient(90deg, rgba(54, 217, 182, 1) 0%, rgba(32, 152, 126, 1), 50%, rgba(0, 212, 255, 1) 100%)"
        header.style.boxShadow = "none"
    }
})
// close windows
const MenuItems = document.querySelectorAll('.navBar .navList ul li');
MenuItems.forEach((item) => {
    item.addEventListener("click", () => {
        Humberger.classList.toggle('active');
        MobileMenu.classList.toggle('active');
    });
});