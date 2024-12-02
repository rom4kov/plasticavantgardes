if (window.innerWidth < 730) {
  console.log("window width under 730")
  const dsNavbar = document.querySelector("#desktop-navbar");
  dsNavbar.classList.add("hidden");
  const mobNavbar = document.querySelector("#mobile-navbar");
  mobNavbar.classList.remove("hidden");
} else {
  const dsNavbar = document.querySelector("#desktop-navbar");
  dsNavbar.classList.remove("hidden");
  const mobNavbar = document.querySelector("#mobile-navbar");
  mobNavbar.classList.add("hidden");
}

window.addEventListener("resize", () => {
  console.log("resize");
  if (window.innerWidth < 730) {
    const dsNavbar = document.querySelector("#desktop-navbar");
    dsNavbar.classList.add("hidden");
    const mobNavbar = document.querySelector("#mobile-navbar");
    mobNavbar.classList.remove("hidden");
  } else {
    const dsNavbar = document.querySelector("#desktop-navbar");
    dsNavbar.classList.remove("hidden");
    const mobNavbar = document.querySelector("#mobile-navbar");
    mobNavbar.classList.add("hidden");
  }
})
