function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

activeItem = null

function buildList() {
    var wrapper = document.getElementById('listWrapper')
    wrapper.innerHTML = ''
    var url = 'http://127.0.0.1:8000/api/TaskList/'
    
    fetch(url)
    .then((response) => response.json())
    .then(function (data) {
        var list = data
        console.log(list)
        for (var i in list) {
            var title = `<span class="title text-white"> ${list[i].title} </span>`
            if (list[i].completed == true) {
                title = `<span class="title text-danger text-decoration-line-through"> ${list[i].title} </span>`
            }
            var item = `
                <div id="data-row-${i}" class="taskWrapper flexWrapper">
                    <div style="flex: 7">
                        ${title}
                    </div>
                    <div style="flex: 1">
                         <button class="btn btn-sm btn-warning edit"> u </button>
                    </div>
                    <div style="flex: 1">
                         <button class="btn btn-sm btn-danger delete"> x </button>
                    </div>
                </div>
            `
            wrapper.innerHTML += item
        }
        for (var i in list) {
            // edit data
            editBtn = document.getElementsByClassName('edit')[i]
            editBtn.addEventListener('click', (function (item) {
                // closure function
                return function () {
                    editTask(item)
                }
            })(list[i]))
            // delete data
            deleteBtn = document.getElementsByClassName('delete')[i]
            deleteBtn.addEventListener('click', (function (item) {
                // closure function
                return function () {
                    deleteTask(item)
                }
            })(list[i]))    
            // Strike Unstrike data
            title = document.getElementsByClassName('title')[i]
            title.addEventListener('click', (function (item) {
                // closure function
                return function () {
                    strikeUnstrike(item)
                }
            })(list[i])) 
        }
    })
    .catch(function(data){
        console.log(data.error)
    })
}
buildList()

function taskSaved() {
    var formWrapper = document.getElementById('formWrapper')
    var form = document.getElementById('form')

    formWrapper.addEventListener('submit', function (event) {
        event.preventDefault()
        var url = 'http://127.0.0.1:8000/api/TaskSaved/'
        if (activeItem != null) {
            var url = `http://127.0.0.1:8000/api/TaskUpdated/${activeItem.id}/`
            activeItem = null
        }

        var title = document.getElementById('title').value
        //var csr = document.querySelector('input[name=csrfmiddlewaretoken]').value
        fetch(url, {
            method: "POST",
            headers: {
                "content-type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({ 'title': title })
        })
        .then(function (response) {
            buildList()
            form.reset()
        })
        .catch(function (response) {
            console.log(response.error)
        })
    })
}
taskSaved()

function editTask(item) {
    activeItem = item
    document.getElementById('title').value = activeItem.title
}

function deleteTask(item) {
    var url = `http://127.0.0.1:8000/api/TaskDeleted/${item.id}/`
    fetch(url, {
        method: "DELETE",
        headers: {
            "content-type": "application/json",
            "X-CSRFToken": csrftoken,
        }
    })
    .then(function (response) {
        buildList()
    })
    .catch(function (response) {
        console.log(response.error);
    })
}

function strikeUnstrike(item) {
    var url = `http://127.0.0.1:8000/api/TaskUpdated/${item.id}/`
    item.completed = !item.completed
    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ 'title': item.title, 'completed': item.completed })
    })
    .then(function (response) {
        buildList()
    })
    .catch(function (response) {
        console.log(response.error);
    })
    console.log('strikeUnstrike', item)
}