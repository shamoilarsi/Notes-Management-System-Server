var gnote = "";

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
    return false;
}

function closeform_editNote() {
    document.querySelector('.bg-modal-edit-note').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal-edit-note').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";
    return false;
}

function closeform_noteclicked() {
    document.querySelector('.bg-modal-noteclick').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal-noteclick').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";
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
    closeform_addNote();
    var uname = getCookie("username");
    var cat = document.getElementById("buttonAddCategory").value;
    var no = document.getElementById("buttonAddNote").value;

    if (no != "") {
        $.ajax({
            url: '/ajax_add_note',
            type: 'post',
            data: {"category": cat, "note": no, "username": uname},
            success: function (data) {
                data = JSON.parse(data)
                alert("Note Added");
                window.location = window.location.pathname;
                return true;
            }
        });
    } else 
        alert("Failed. Note Empty");

    return false;
}

function signout() {
    setCookie('username', '', 0); // this will delete the cookie.
    setCookie('password', '', 0); // this will delete the cookie.
    window.location = "/login";
}

function noteClick(note) {
    gnote = note

    document.querySelector('.bg-modal-noteclick').style.display = "flex";
    document.querySelector('.bg-modal-noteclick').style.animation = "fade-in 0.3s";

    document.querySelector('body').style.overflow = "hidden";
    return false;
}

function deleteNote() {
    closeform_noteclicked()
    $.ajax({
        url: '/ajax_delete_note',
        type: 'post',
        data: {note: gnote, username: uname},
        success: function (data) {
            data = JSON.parse(data)
            alert("Note Deleted")
            window.location = window.location.pathname
        }
    });
}

function show_editNode_form() {
    closeform_noteclicked();
    document.querySelector('.bg-modal-edit-note').style.display = "flex";
    document.querySelector('.bg-modal-edit-note').style.animation = "fade-in 0.3s";
    document.querySelector('body').style.overflow = "hidden";

    document.getElementById('buttonEditNote').value = gnote.trim();
    return true;
}

function editNote_submitted() {
    var newnote = document.getElementById('buttonEditNote').value;
    closeform_editNote();

    $.ajax({
        url: '/ajax_edit_note',
        type: 'post',
        data: {oldnote: gnote, newnote: newnote, username: uname},
        success: function (data) {
            data = JSON.parse(data)
            alert("Note Edited");
            window.location = window.location.pathname;
            return true;
        }
    });
}