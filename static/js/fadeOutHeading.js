function fadeOutOnScroll(fadeHeight) {
    const heading = document.querySelector(".text-6xl");
    const writeContainer = document.querySelector("#write-container");
    console.log(writeContainer)
    let previousScrollY = window.scrollY;
    let lastKnownScrollPosition = 0;
    let ticking = false;

    function getElementScrollHeight(writeContainer) {
        var rect = writeContainer.getBoundingClientRect();
        console.log(rect.y)
        return rect.y;
    }

    window.addEventListener('scroll', function() {
        let currentScrollY = window.scrollY;

        if (!ticking) {
            window.requestAnimationFrame(() => {
                doSomething(lastKnownScrollPosition);
                ticking = false;
            });

            ticking = true;
        }

        const elementHeight = getElementScrollHeight(writeContainer);
        if (currentScrollY > previousScrollY && elementHeight < fadeHeight) {
            const opacity = (elementHeight - 300) / (fadeHeight - 300);
            console.log("scrollY:", currentScrollY);
            console.log("elementHeight:", elementHeight);
            heading.style.opacity = opacity;
        } else if (currentScrollY < previousScrollY && elementHeight < fadeHeight) {
            const opacity = (elementHeight - 200) / (fadeHeight - 300);
            console.log(currentScrollY);
            heading.style.opacity = opacity;
        } else {
            heading.style.opacity = 1;
        }

        previousScrollY = currentScrollY;
    });
}

fadeOutOnScroll(500); // Change 300 to your desired height
