
function favourites() {
    var f = document.getElementsByClassName("favorites");
    var p = document.getElementsByClassName("purchase");
    p[0].style.display = "none";
    f[0].style.display = "grid";
}

function purchase() {
    var f = document.getElementsByClassName("favorites");
    var p = document.getElementsByClassName("purchase");
    f[0].style.display = "none";
    p[0].style.display = "grid";
}