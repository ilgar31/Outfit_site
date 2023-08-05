
function favourites() {
    var f = document.getElementsByClassName("favorites");
    var p = document.getElementsByClassName("purchase");
    var f_button = document.getElementsByClassName("items_far");
    var p_button = document.getElementsByClassName("items_pur");
    p[0].style.display = "none";
    f[0].style.display = "grid";
    f_button[0].style.backgroundColor = '#c5c4c4';
    p_button[0].style.backgroundColor = '#D9D9D9';
}

function purchase() {
    var f = document.getElementsByClassName("favorites");
    var p = document.getElementsByClassName("purchase");
    var f_button = document.getElementsByClassName("items_far");
    var p_button = document.getElementsByClassName("items_pur");
    f[0].style.display = "none";
    p[0].style.display = "grid";
    console.log(f_button)
    f_button[0].style.backgroundColor = '#D9D9D9';
    p_button[0].style.backgroundColor = '#c5c4c4';
}