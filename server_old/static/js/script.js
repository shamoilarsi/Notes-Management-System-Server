function checkLogin() {
    var l = document.getElementById("password").value;
    var n = l.length;

    if (n < 8) {
        document.getElementById("password").className = document.getElementById("password").className + " error";  // this adds the error class
        document.getElementById("password").placeholder = "8 digits or more";
        document.getElementById("password").value = "";
        return false;
    } else {
        document.getElementById("password").className = document.getElementById("password").className.replace(" error", ""); // this removes the error class

        $.ajax({
            url: '/jlogin',
            type: 'post',
            data: {username: $('input[name="uname"]').val(), password: $('input[name="pass"]').val()},
            success: function (data) {

                if (!data.status) {
                    document.getElementById("alert").innerHTML = data.alert;
                    return false;
                } else {
                    document.cookie = "username=" + data.uname;
                    document.cookie = "password=" + data.password;
                    window.location = "/main/" + data.uname;
                    return true;
                }

            }
        });
    }

}


function checkNewAcc() {
    var l = document.getElementById("password").value;
    var n = l.length;

    if (n < 8) {
        document.getElementById("password").className = document.getElementById("password").className + " error";  // this adds the error class
        document.getElementById("password").placeholder = "8 digits or more";
        document.getElementById("password").value = "";
        return false;
    } else {
        document.getElementById("password").className = document.getElementById("password").className.replace(" error", ""); // this removes the error class

        $.ajax({
            url: '/jnewacc',
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
                if (!data.status) {
                    document.getElementById("alert").innerHTML = data.alerttext;
                    document.getElementById("alert").color = data.color;
                    return false;
                } else {
                    document.cookie = "username=" + data.uname;
                    document.cookie = "password=" + data.password;
                    window.location = "/main/" + data.uname;
                    return true;
                }

            }
        });
    }
}

//
// $(function() {
//   $('.textOfButton').hover(function() {
//     document.getElementById("half-out-button").style.boxShadow = "0px 0px 5px black";
//
//   }, function() {
//     // on mouseout, reset the background colour
//     document.getElementById("half-out-button").style.boxShadow = "";
//   });
// });
//
function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay) ;
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length >= 2) return parts.pop().split(";").shift();
}

function add() {
    document.querySelector('.bg-modal').style.display = "flex";
    document.querySelector('.bg-modal').style.animation = "fade-in 0.3s";
    document.querySelector('body').style.overflow = "hidden";
    return false;
}

function closeform() {
    document.querySelector('.bg-modal').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";
    return false;
}

function closeform_editNote() {
    document.querySelector('.bg-modal-editNote').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal-editNote').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";
    return false;
}

function addNote() {
    closeform();
    var uname = getCookie("username");
    var no = document.getElementById("buttonAddNote").value;

    if (no != "") {
        $.ajax({
            url: '/jaddNote',
            type: 'post',
            data: {note: no, username: uname},
            success: function (data) {
                alert("Note Added");
                window.location = window.location.pathname;
                return true;
            }
        });
    } else {
        alert("Failed. Note Empty");
    }
}


function setCookie(cname, cvalue, exMins) {
    var d = new Date();
    d.setTime(d.getTime() + (exMins * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


function signout() {
    setCookie('username', '', 0); // this will delete the cookie.
    setCookie('password', '', 0); // this will delete the cookie.
    window.location = "/login";
}

var gnote = "";

function noteClick(note) {

    gnote = note;

    document.querySelector('.bg-modal-noteclick').style.display = "flex";
    document.querySelector('.bg-modal-noteclick').style.animation = "fade-in 0.3s";

    document.querySelector('body').style.overflow = "hidden";
    //document.getElementById("forFont").innerHTML = "<p id='note-in-form' class='note-in-form'>"+note+"</p>";
    //alert("<p id='note-in-form' class='note-in-form'>"+note+"</p>");

    return false;
}

function deleteNote() {

    closeform_noteclicked();

    $.ajax({
        url: '/jdeleteNote',
        type: 'post',
        data: {note: gnote, username: uname},
        success: function (data) {
            alert("Note Deleted");
            window.location = window.location.pathname;
            return true;
        }
    });
}

function editNote() {

    closeform_noteclicked();
    document.querySelector('.bg-modal-editNote').style.display = "flex";
    document.querySelector('.bg-modal-editNote').style.animation = "fade-in 0.3s";
    document.querySelector('body').style.overflow = "hidden";

    document.getElementById('buttonEditNote').value = gnote;
    return true;
}


function editNoteF() {

    var newnote = document.getElementById('buttonEditNote').value;

    closeform_editNote();

    $.ajax({
        url: '/jeditNote',
        type: 'post',
        data: {oldnote: gnote, newnote: newnote, username: uname},
        success: function (data) {
            alert("Note Edited");
            window.location = window.location.pathname;
            return true;
        }
    });
}


function closeform_noteclicked() {
    document.querySelector('.bg-modal-noteclick').style.animation = "fade-out 0.3s";
    document.querySelector('.bg-modal-noteclick').style.display = "none";
    document.querySelector('body').style.overflow = "scroll";
    return false;
}
