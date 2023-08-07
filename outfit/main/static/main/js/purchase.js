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

function minuscount(n) {
    const count = document.getElementById("count" + n).innerHTML;
    if (count == 1) {
        return;
    }
        $.ajax({
        type: "POST",
        url: url,
        data: {
            "csrfmiddlewaretoken": csrf,
            "id": n,
            "type": "change_count",
            "operation": "minus",
        },
        success: (res)=> {
            document.getElementById("count" + n).innerHTML = `${res.item_count}`
            var items = document.getElementsByClassName("cost");
            for (i = 0; i < items.length; i++) {
              items[i].innerHTML = `${res.cost}руб`;
            }
        },
        error: (err)=> {
            console.log("error")
        }
    })
}

function pluscount(n) {
    const count = document.getElementById("count" + n).innerHTML;
    $.ajax({
        type: "POST",
        url: url,
        data: {
            "csrfmiddlewaretoken": csrf,
            "id": n,
            "type": "change_count",
            "operation": "plus",
        },
        success: (res)=> {
            document.getElementById("count" + n).innerHTML = `${res.item_count}`
            var items = document.getElementsByClassName("cost");
            for (i = 0; i < items.length; i++) {
              items[i].innerHTML = `${res.cost}руб`;
            }
        },
        error: (err)=> {
            console.log(err)
            console.log("error")
        }
    })
}