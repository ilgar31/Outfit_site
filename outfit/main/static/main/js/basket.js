function removeitem(n) {
    const item = document.getElementById("item" + n);
    console.log(item)
    $.ajax({
        type: "POST",
        url: url,
        data: {
            "csrfmiddlewaretoken": csrf,
            "id": n,
            "type": "delete",
        },
        success: (res)=> {
            console.log(res)
            item.remove()
            document.getElementById("cost").innerHTML = `
                <p class="count_items">Товары, ${res.count} шт</p>
                <p class="count_cost">${res.cost} руб</p>
                <p class="itog">Итого</p>
                <p class="cost_value">${res.cost} руб</p>
            `
            if (res.count == 0) {
                document.getElementById("content").innerHTML = `
                    <p class="basket_title">Корзина</p>
                    <div class="wrapper">
                        <a href="/" class="add_items"><p>Добавить товары</p></a>
                    </div>
                `
            }
        },
        error: (err)=> {
            console.log("error")
        }
    })
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
            document.getElementById("cost").innerHTML = `
                <p class="count_items">Товары, ${res.count} шт</p>
                <p class="count_cost">${res.cost} руб</p>
                <p class="itog">Итого</p>
                <p class="cost_value">${res.cost} руб</p>
            `
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
            document.getElementById("cost").innerHTML = `
                <p class="count_items">Товары, ${res.count} шт</p>
                <p class="count_cost">${res.cost} руб</p>
                <p class="itog">Итого</p>
                <p class="cost_value">${res.cost} руб</p>
            `
        },
        error: (err)=> {
            console.log("error")
        }
    })
}