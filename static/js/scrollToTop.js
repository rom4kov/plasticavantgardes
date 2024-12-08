const scrollToTopBtn = document.querySelector('#scroll-to-top');

function scrollToTop() {
    window.scroll(0, 0);
}

const options2 = {
    root: null,
    threshold: 0,
    rootMargin: "0px"
};

const observer3 = new IntersectionObserver(function (entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            scrollToTopBtn.classList.remove('opacity-100');
            scrollToTopBtn.classList.add('opacity-0');
            scrollToTopBtn.style.cursor = 'default';
            scrollToTopBtn.removeEventListener('click', scrollToTop)
        } else {
            scrollToTopBtn.classList.remove('opacity-0');
            scrollToTopBtn.classList.add('opacity-100');
            scrollToTopBtn.style.cursor = 'pointer';
            scrollToTopBtn.addEventListener('click', scrollToTop)
        };
    });
}, options2)

const topImage = document.querySelector('#top-image');

if (topImage) {
    observer3.observe(topImage);
}

