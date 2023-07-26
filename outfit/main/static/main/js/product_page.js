var slideIndex = 0;
showSlides(slideIndex);

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");

  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex].style.display = "block";
  dots[slideIndex].className += " active";
}


var type_size = 0;
showSize(type_size);

function currentSize(n) {
    showSize(type_size = n);
}

function showSize(n) {
  var i;
  var types = document.getElementsByClassName("type_size");
  var dots = document.getElementsByClassName("type_button");

  for (i = 0; i < types.length; i++) {
      types[i].style.display = "none";
  }
  types[type_size].style.display = "inline-block";
}


const BuyButton = document.getElementById("buy_button")
const BuyFrom = document.getElementById("buy_form")


BuyButton.addEventListener('click', e=> {

})
