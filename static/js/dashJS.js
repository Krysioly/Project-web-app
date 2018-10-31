let publish = $('#publish'); //submit button id
let enrtyDiv = $('#entry-div'); //div with form id

function changeDiv(results) {
    console.log(results);
    console.log(results['title']);
    console.log(results['text']);
    $('#finishedTitle').html(results['title']);
    $('#finishedText').html(results['text']);
    $('#entry-div').hide();
}

function updateDiv(evt) {
    evt.preventDefault();

    let entryInput = {
        "title" : $('#title').val(),
        "text" : $('#base-text').val(),
    };
    
    $.post("/post-entry", entryInput ,changeDiv);
}

publish.on('click', updateDiv);
/////////////////////////////////////////

let todoList = $('#todoList'); //ul id
let update = $('#update'); //submit id

function appendTodo(results) {
    console.log(results);
    $('#todoList').append("<li>"+results+"</li>");
}

function updateTodo(evt) {
    evt.preventDefault();

    let todoInput = {
        "todo" : $('#todo').val(),
    };
    
    $.post("/update-todo", todoInput ,appendTodo);
    document.forms["todoForm"].reset();
}

update.on('click', updateTodo);
/////////////////////////////////////////////////

// Get the element, add a click listener...
$("#todoList").on("click", function(e) {
    // e.target is the clicked element!
    // If it was a list item
    if(e.target && e.target.nodeName == "LI") {
        // List item found!  Output the ID!
        console.log("List item ", e.target.id.replace("post-", ""), " was clicked!");
        e.target.remove();
        let todoItemdict = { "todoItem" : e.target.id};
        $.post("/delete-todo", todoItemdict, console.log("working"));
    }
});

/////////////////////////////////////////////////////////////

function changeNewsCat(results) {
    console.log(results);
    $('#categorynews').html(results);
}

function updateNewsCat(evt) {
    evt.preventDefault();

    let searchCat = {'category' : $('#radioCat').val(),};
    console.log(searchCat)
    
    $.get("/search-category", searchCat ,changeNewsCat);
}

$('#searchcat').on('click', updateNewsCat);

//////////////////////////////////////

function changeNewsKey(results) {
    console.log(results);
    $('#keywordnews').html(results);
    $('#newsinput').hide();
}

function updateNewsKey(evt) {
    evt.preventDefault();

    let searchKey = $('#keyword').val();
    
    $.get("/search-keyword", searchKey ,changeNewsKey);
}

$('#searchkey').on('click', updateNewsKey);

