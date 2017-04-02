function HamburgerClick(){

    // Toggle class "is-active"
    document.querySelector(".hamburger").classList.toggle("is-active");

    scrollTo(0,0);

    // var nav = document.getElementsByTagName("nav")[0];
    document.querySelector("nav").classList.toggle("nav_open");

}