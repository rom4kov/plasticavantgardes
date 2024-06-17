function fadeOutOnScroll(elementClass, fadeHeight) {
    const elements = document.querySelectorAll(elementClass);
    console.log(elements);
    let previousScrollY = window.scrollY;
    let lastKnownScrollPosition = 0;
    let ticking = false;

    function getElementScrollHeight(element) {
        var rect = element.getBoundingClientRect();
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

        for (let element of elements) {
            const elementHeight = getElementScrollHeight(element);
            if (currentScrollY > previousScrollY && elementHeight < fadeHeight) {
                const opacity = (elementHeight - 300) / (fadeHeight - 300);
                console.log("scrollY:", currentScrollY);
                console.log("elementHeight:", elementHeight);
                element.style.opacity = opacity;
            } else if (currentScrollY < previousScrollY && elementHeight < fadeHeight) {
                const opacity = (elementHeight - 300) / (fadeHeight - 300);
                console.log(currentScrollY);
                element.style.opacity = opacity;
            } else {
                element.style.opacity = 1;
            }
        }

        previousScrollY = currentScrollY;
    });
}

fadeOutOnScroll('.article-card', 500); // Change 300 to your desired height
