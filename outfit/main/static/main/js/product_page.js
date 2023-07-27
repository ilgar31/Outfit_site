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
const size_types = $('input[name="radio"]');
var size_type;
const Rsizes = $('input[name="RU"]');
const Esizes = $('input[name="EU"]');
var Rsize;
var Esize;


BuyButton.addEventListener('click', e=> {

    for (i = 0; i < size_types.length; i++) {
        if (size_types[i].checked) {
            size_type = size_types[i].value;
        }
    }

    for (i = 0; i < Rsizes.length; i++) {
        if (Rsizes[i].checked) {
            Rsize = Rsizes[i].value;
        }
    }

    for (i = 0; i < Esizes.length; i++) {
        if (Esizes[i].checked) {
            Esize = Esizes[i].value;
        }
    }
    $.ajax({
        type: "POST",
        url: url,
        data: {
            "csrfmiddlewaretoken": csrf,
            'type_size': size_type,
            'RU_size': Rsize,
            'EU_size': Esize,
        },
        success: (res)=> {
            console.log("added")
        },
        error: (err)=> {
            console.log("error")
        }
    })
})
