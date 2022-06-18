const openDoor = document.querySelector(".button_open_door");
const closeDoor = document.querySelector(".button_close_door");
const confirm = document.querySelector(".button_confirm");
const change_password = document.querySelector(".button_change_password");
let input = document.getElementById('textbox_id');
const input_password = document.getElementById('set_new_password');

let password_agreed = false

confirm.addEventListener('click', () => {
    let input_data = input.value
    if (input_data !== "") {
        sendCommandToServer(input_data)
        input.value = "";
    }
})


let open_door = false
openDoor.addEventListener('click', () => {
    password_agreed = false;
    sendCommandToServer("start_red")
    confirm.disabled = false;
    input.disabled = false;
    setTimeout(() => {
        if (password_agreed !== true) {
            sendCommandToServer("buzz")
            alert("time lost")
            confirm.disabled = true
        }
    }, 20000);
    open_door = true
});


let close_door = false
closeDoor.addEventListener('click', () => {
    password_agreed = false
    confirm.disabled = false
    setTimeout(() => {
        if (password_agreed !== true) {
            alert("time lost")
            confirm.disabled = true
        }
    }, 20000);
    close_door = true
});


change_password.addEventListener('click', () => {
    let input_data = input_password.value
    if (input_data !== "") {
        sendChangePasswordToServer(input_data)
        input_password.value = '';
    }
})


function sendCommandToServer(command) {
    command = command.toString()
    console.log(command)
    fetch("http://127.0.0.1:5000/home", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(command)
    }).then(function (response) {
        console.log(response.status)
        if (response.status === 201) {
            password_agreed = true
            if (open_door === true) {
                sendCommandToServer("remove_alarm")
                alert("open door")
                input_password.disabled = false;
                change_password.disabled = false;
                open_door = false
            } else if (close_door === true) {
                sendCommandToServer("set_alarm")
                change_password.disabled = true;
                input_password.disabled = true;
                alert("close door")
                close_door = false
            }
            confirm.disabled = true
        } else if (response.status === 202) {
            alert("password is not correct")
            confirm.disabled = true
        }
    })
}

function sendChangePasswordToServer(command) {
    fetch("http://127.0.0.1:5000/change_password", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(command)
    }).then(function (response) {
        console.log(response.status)
        if (response.status === 200) {
            alert("password changed")
        }
    })
}

