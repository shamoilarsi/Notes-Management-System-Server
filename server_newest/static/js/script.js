var gnote = "";
var gcategory = "";
var close_modal = false;

function validate_login() {
    $.ajax({
        url: '/ajax_validate_login',
        type: 'post',
        data: {username: $('input[name="uname"]').val(), password: $('input[name="pass"]').val()},
        success: function (data) {
            data = JSON.parse(data)
            if (!data.status) {
                document.getElementById("alert").innerHTML = data["alert_text"];
            } else {
                document.cookie = "username=" + data.uname;
                document.cookie = "password=" + data.password;
                window.location = "/main/" + data.uname;
            }
        }
    });
    return false;
}

function validate_newacc() {
    $.ajax({
        url: '/ajax_validate_newacc',
        type: 'post',
        data: {
            fname: $('input[name="fname"]').val(),
            lname: $('input[name="lname"]').val(),
            email: $('input[name="email"]').val(),
            phone: $('input[name="phone"]').val(),
            username: $('input[name="uname"]').val(),
            password: $('input[name="pass"]').val(),
            sques: $('input[name="sques"]').val(),
            ans: $('input[name="ans"]').val()
        },
        success: function (data) {
            console.log(typeof data)
            data = JSON.parse(data)
            if (!data.status) {
                document.getElementById("alert").innerHTML = data["alert_text"];
                document.getElementById("alert").color = data["color"];
            } else {
                document.cookie = "username=" + data.uname;
                document.cookie = "password=" + data.password;
                window.location = "/main/" + data.uname;
            }
        }
    });
    return false;
}

function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay) ;
}

function setCookie(cname, cvalue, exMins) {
    var d = new Date();
    d.setTime(d.getTime() + (exMins * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length >= 2) return parts.pop().split(";").shift();
}

function closeform_addNote() {
    document.querySelector('.bg-modal-add-note').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal-add-note').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";

    window.location = window.location.pathname;
    return false;
}

function closeform_editNote() {
    document.querySelector('.bg-modal-edit-note').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal-edit-note').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";

    window.location = window.location.pathname;
    return false;
}

function closeform_noteclicked() {
    document.querySelector('.bg-modal-noteclick').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal-noteclick').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";

    if (close_modal)
        window.location = window.location.pathname;
    return false;
}

function forgotpassword(){
    alert("puk")
    
    return false;
}

function show_addNote_form() {
    document.querySelector('.bg-modal-add-note').style.display = "flex";
    document.querySelector('.bg-modal-add-note').style.animation = "fade-in 0.3s";
    document.querySelector('body').style.overflow = "hidden";
    return false;
}

function actually_addNote() {
    // closeform_addNote();
    var uname = getCookie("username");
    var cat = document.getElementById("buttonAddCategory").value;
    var no = document.getElementById("buttonAddNote").value;

    if (no != "" && cat != "") {
        $.ajax({
            url: '/ajax_add_note',
            type: 'post',
            data: {"category": cat, "note": no, "username": uname},
            success: function (data) {
                data = JSON.parse(data)
                document.getElementById('ButtonActuallyAddNote').style.backgroundColor = "#5cb85c";
                document.getElementById("ButtonActuallyAddNote").disabled = true;
                document.getElementById('ButtonActuallyAddNote').innerHTML = "Note Added";

                // sleep(2000);
                // alert("Note Added");
                // window.location = window.location.pathname;
                return false;
            }
        });
    } else {
        document.getElementById('ButtonActuallyAddNote').style.backgroundColor = "red";
        document.getElementById('ButtonActuallyAddNote').innerHTML = "Failed";
    }

    return false;
}

function signout() {
    setCookie('username', '', 0); // this will delete the cookie.
    setCookie('password', '', 0); // this will delete the cookie.
    window.location = "/login";
}

function noteClick(category, note) {
    gnote = note
    gcategory = category

    document.querySelector('.bg-modal-noteclick').style.display = "flex";
    document.querySelector('.bg-modal-noteclick').style.animation = "fade-in 0.3s";

    document.querySelector('body').style.overflow = "hidden";
    return false;
}

function deleteNote() {
    close_modal = true;
    $.ajax({
        url: '/ajax_delete_note',
        type: 'post',
        data: {note: gnote},
        success: function (data) {
            data = JSON.parse(data)
            document.getElementById('deleteText').style.color = "green";
            document.getElementById('deleteText').innerText = "DELETED SUCCESSFULLY";
        }
    });
}

function show_editNode_form() {
    close_modal = false;
    closeform_noteclicked();
    document.querySelector('.bg-modal-edit-note').style.display = "flex";
    document.querySelector('.bg-modal-edit-note').style.animation = "fade-in 0.3s";
    document.querySelector('body').style.overflow = "hidden";

    document.getElementById('inputEditNote').value = gnote.trim();
    document.getElementById('inputEditCategory').value = gcategory.trim();
    return false;
}

function editNote_submitted() {
    var newcategory = document.getElementById('inputEditCategory').value;
    var newnote = document.getElementById('inputEditNote').value;
    // closeform_editNote();

    $.ajax({
        url: '/ajax_edit_note',
        type: 'post',
        data: {oldnote: gnote, new_note: newnote, newcat:newcategory},
        success: function (data) {
            data = JSON.parse(data)
            if (data.status){
                document.getElementById('ButtonEditNote').style.backgroundColor = "#5cb85c";
                document.getElementById("ButtonEditNote").disabled = true;
                document.getElementById('ButtonEditNote').innerHTML = "Noted Editted";
            }
            else {
                document.getElementById('ButtonEditNote').style.backgroundColor = "red";
                document.getElementById("ButtonEditNote").disabled = true;
                document.getElementById('ButtonEditNote').innerHTML = "Failed";
            }
            return false;
        }
    });
    return false;
}