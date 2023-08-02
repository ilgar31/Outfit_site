var itemIndex = 0;
showItem(itemIndex);

function plusItem(n) {
  showItem(itemIndex += n);
}

function showItem(n) {
  var i;
  var items = document.getElementsByClassName("items_box");
  if (n > items.length - 1) {itemIndex = 0}
  if (n < 0) {itemIndex = items.length - 1}
  for (i = 0; i < items.length; i++) {
      items[i].style.display = "none";
  }
  console.log(items[itemIndex])
  console.log(itemIndex)
  items[itemIndex].style.display = "block";
}