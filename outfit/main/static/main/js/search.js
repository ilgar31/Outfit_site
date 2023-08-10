const url = window.location.href
const searchInput = document.getElementById("search_input")
const resultsBox = document.getElementById("results_box")

const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value


const sendSearchData = (item) => {
    $.ajax({
        type: "POST",
        url: '/search/',
        data: {
            "csrfmiddlewaretoken": csrf,
            'item': item,
            "type": "elements",
        },
        success: (res)=> {
            console.log(res.item)
            const data = res.item
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ''
                data.forEach(item=> {
                    resultsBox.innerHTML += `
                        <a href="${item.url}" class="item_in_search">
                            <div class="item_box_search">
                                <div class="item_img_box_search">
                                    <img src="${item.image}" class='item_img_search'>
                                </div>
                                <div class="item_name_box_search">
                                    <h5 class="name_item_search">${item.name}</h5>
                                </div>
                            </div>
                        </a>
                    `
                })
            }
            else {
                if (searchInput.value.length > 0) {
                    resultsBox.innerHTML = `<d>${data}<\d>`
                }
                else {
                    resultsBox.classList.add('not-visible')
                }
            }
        },
        error: (err)=> {
            console.log(err)
        }
    })
}

const searchPage = (item) => {
    $.ajax({
        type: "POST",
        url: "/search_page/",
        data: {
            "csrfmiddlewaretoken": csrf,
            'item': item,
        },
        success: (res)=> {
            console.log(res.items)
            if (res.bool) {
                window.location.replace(res.url)
            }
        },
        error: (err)=> {
            console.log(err)
        }
    })
}


const showData = () => {
    $.ajax({
        type: "POST",
        url: '/search/',
        data: {
            "csrfmiddlewaretoken": csrf,
            'type': 'data',
        },
        success: (res)=> {
            resultsBox.innerHTML = ''
            if (res.history.length) {
                resultsBox.innerHTML += `
                    <p class='search_title'>Недавние поисковые запросы</p>
                `
                res.history.forEach(text=> {
                    var url_text = '/goods/' + text;
                    resultsBox.innerHTML += `
                        <a href=${url_text} class="history_object">
                            <p>${text}</p>
                        </a>
                    `
                })
            }
            resultsBox.innerHTML += `
                <p class='search_title'>Подборки для Вас</p>
            `
            res.items_for_you.forEach(item=> {
                resultsBox.innerHTML += `
                    <a href="${item.url}" class="item_in_search">
                        <div class="item_box_search">
                            <div class="item_img_box_search">
                                <img src="${item.image}" class='item_img_search'>
                            </div>
                        </div>
                    </a>
                `
            })

            resultsBox.innerHTML += `
                <p class='search_title'>Часто просматриваемое</p>
            `
        },
        error: (err)=> {
            console.log(err)
        }
    })
}


searchInput.addEventListener('keyup', e=> {
    console.log(e.target.value)

    if (resultsBox.classList.contains("not-visible")) {
        resultsBox.classList.remove('not-visible')
    }

    if (searchInput.value && (e.key === 'Enter' || e.keyCode === 13)) {
        searchPage(e.target.value)
    }
    else {
        sendSearchData(e.target.value)
    }
})

window.addEventListener('click', e=> {
    if (!($('#search_input').is(":focus"))) {
        resultsBox.classList.add('not-visible')
    }
    if ($('#search_input').is(":focus") && !searchInput.value) {
        resultsBox.classList.remove('not-visible')
        showData()
    }
    else if ($('#search_input').is(":focus")) {
        resultsBox.classList.remove('not-visible')
    }
})
