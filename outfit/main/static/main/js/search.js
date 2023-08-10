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
                data.forEach(text=> {
                    var url_text = '/goods/' + text.replaceAll(" ", "%20");;
                    resultsBox.innerHTML += `
                        <a href=${url_text} class="item_in_search">
                            <div class="item_box_search">
                                <img src="${res.lupa}" class='item_img_search'>
                                <h5 class="name_item_search">${text}</h5>
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


const delete_search = (text) => {
    $.ajax({
        type: "POST",
        url: "/delete_search/",
        data: {
            "csrfmiddlewaretoken": csrf,
            'search_text': text,
        },
        success: (res)=> {
            console.log('sldkfj')
            resultsBox.classList.remove('not-visible')
            showData()
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
                    var url_text = '/goods/' + text.replaceAll(" ", "%20");;
                    resultsBox.innerHTML += `
                        <div class="history_object">
                            <div class="history_element">
                                <a href=${url_text}>
                                    <p style="vertical-align: middle;float:left; margin-block-start:0; margin-right: 20px; color: black;">${text}</p>
                                </a>
                                <button class='btn_delete' style="vertical-align: middle;float:right;" onclick="delete_search('${text}')"><img src="${res.delete_search}" class='delete_search'></button>
                            </div>
                        </div>
                    `
                })
            }
            resultsBox.innerHTML += `
                <p class='search_title'>Подборки для Вас</p>
            `

            res.items_for_you.forEach(item=> {
                resultsBox.innerHTML += `
                    <a href="${item.url}" class="item_in_search">
                        <div class="item_for_you">
                            <img src="${item.image}" class='img_for_you'>
                        </div>
                    </a>
                `
            })

            resultsBox.innerHTML += `
                <p class='search_title'>Часто просматриваемое</p>
            `

            res.items_top.forEach(item=> {
                resultsBox.innerHTML += `
                    <a href="${item.url}" class="item_in_search">
                        <div class="item_for_you">
                            <img src="${item.image}" class='img_for_you'>
                        </div>
                    </a>
                `
            })
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
