// Login and signup button behaviour
document.querySelector(".login").addEventListener("click", function() {
    document.querySelectorAll(".modal")[0].className += " is-active"
});

document.querySelectorAll(".modal-close")[0].addEventListener("click", function() {
    document.querySelectorAll(".modal")[0].classList.remove("is-active")
});

document.querySelector(".signup").addEventListener("click", function() {
    document.querySelectorAll(".modal")[1].className += " is-active"
});

document.querySelectorAll(".modal-close")[1].addEventListener("click", function() {
    document.querySelectorAll(".modal")[1].classList.remove("is-active")
})

// Participate button behavior
document.querySelector(".participate").addEventListener("click", function() {
    document.querySelector(".participate").remove()
    var newButton = document.createElement('button')
    document.querySelector(".card-header").appendChild(newButton)
    newButton.textContent = "참여완료"
    newButton.className = "button is-light"
})

// Gather button behavior
document.querySelector(".gather").addEventListener("click", function() {
    document.querySelector(".gathering-form").className += " is-active"
})

document.querySelector(".gathering-form-close").addEventListener("click", function() {
    document.querySelector(".gathering-form").classList.remove("is-active")
});

// Gathering form behavior
document.querySelector(".dropdown").addEventListener("click", function() {
    document.querySelector(".dropdown").className += " is-active"
})

// Signup form behavior
document.querySelector(".signup-button").addEventListener("click", function() {
    let name = document.querySelector(".signup-name").value
    let email = document.querySelector(".signup-email").value
    let password = document.querySelector(".signup-password").value

    $.ajax({
        type: "POST",
        url: "/signup",
        data: { name_give: name, email_give: email, password_give: password},
        success: function(response){
            if (response["result"] == "success") {
                alert("회원가입 성공! 이제 로그인해주세요.");
                window.location.reload();
            } else {
                alert("다시 시도해주세요!") //이미 가입된 아이디입니다. 부분 넣어야함
            }
        }
    })
})

// Login form behavior
document.querySelector(".login-button").addEventListener("click", function() {
    let email = document.querySelector(".login-email").value
    let password = document.querySelector(".login-password").value

    $.ajax({
        type: "POST",
        url: "/login",
        data: { email_give: email, password_give: password},
        success: function(response){
            if (response["result"] == "success") {
                alert("로그인 성공!");
                window.location.reload();

                // Save jwt token
                // token = token from server
                // document.cookie = "token=" + token
            } else {
                alert("아이디나 비밀번호가 틀렸습니다.")
            }
        }
    })
})

