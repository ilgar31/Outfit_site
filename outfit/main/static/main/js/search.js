const url = window.location.href
const searchForm = document.getElementById("search_form")
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


searchInput.addEventListener('keyup', e=> {
    console.log(e.target.value)

    if (resultsBox.classList.contains("not-visible")) {
        resultsBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
})

window.addEventListener('click', e=> {
    if (!($('#search_input').is(":focus"))) {
        resultsBox.classList.add('not-visible')
    }
})
