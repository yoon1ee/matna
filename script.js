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

// Card listing behavior
// $.ajax({
//     type: "GET",
//     url: "/listing",
//     data: {},
//     success: function(response) {
//         let memo = response["memo"];
//         for (let i = 0; i < memo.length; i++) {
//             makeCard(memo[i]["restaurant_name"], memo[i]["restaurant_photo"], memo[i]["like_number"], memo[i]["gathering"], memo[i]["meeting_time"], memo[i]["participants_number"], memo[i]["participants_name"])
//         }
//     }
// })

restaurant_name = "샘플식당"
restaurant_photo = "restaurant_3.png"
like_number = 11
gathering = "Y"
meeting_time = "12:00"
participants_number = 3
participants_name = ["철수", "영희"]

makeCard(restaurant_name, restaurant_photo, like_number, gathering, meeting_time, participants_number, participants_name)

function makeCard(restaurant_name, restaurant_photo, like_number, gathering, meeting_time, participants_number, participants_name) {
    let color = "";
    let status = "";
    if (gathering === "Y") {
        color = "green"
        status = "모집중"
    } else {
        color = "red"
        status = "모집없음"
    }
    let participants_count = participants_name.length

    let temp_html = `<div class="column is-one-third">
                        <div class="card">
                        <header class="card-header">
                            <p class="card-header-title">
                            <i style="color: ${color}; margin-right: 10px;" class="fas fa-circle"></i>
                            <span class="gathering-status">${status}</span>
                            <span class="participants-status" title="참가자: ${participants_name}"> ${participants_count}/${participants_number}</span>
                            <span class="gathering-time">${meeting_time}</span>
                            </p>
                            <button class="button is-black participate">참여하기</button>
                        </header>
                        <div class="card-image">
                            <figure class="image is-4by3">
                            <img src="${restaurant_photo}" alt="Placeholder image">
                            </figure>
                        </div>
                        <div class="card-content">
                            <div class="media">
                            <div class="media-content">
                                <p class="title is-4">${restaurant_name}</p>
                            </div>
                            </div>
                            <div class="content">
                            <i class="fas fa-thumbs-up"></i>
                            <span class="like-count">${like_number}</span>
                            </div>
                        </div>
                    </div>`
    $(".columns").append(temp_html);
}

// Participate button behavior
const participateButtons = document.querySelectorAll(".participate")
//add resID and token to back

$.ajax({
    type: "POST",
    url: "/participate_check",
    data: {},
    success: function(response) {
        if (response["result"] == "success") {
            for (let i = 0; i < participateButtons.length; i++) {
                participateButtons[i].addEventListener("click", function() {
                    var oldbutton = this.parentElement.querySelector(".button")
                    var newButton = document.createElement('button')
                    newButton.textContent = "참여완료"
                    newButton.className = "button is-light"
                    this.parentElement.parentElement.querySelector(".card-header").appendChild(newButton)
                    oldbutton.remove()
                })
            }
        } else {
            alert("먼저 로그인을 해주세요!")
        }
    }
})

// Like button behavior
const likeButtons = document.querySelectorAll(".like-button")
//add resID and token to back

$.ajax({
    type: "POST",
    url: "/participate_check",
    data: {},
    success: function(response) {
        if (response["result"] == "success") {
            for (let i = 0; i < likeButtons.length; i++) {
                likeButtons[i].addEventListener("click", function() {
                    window.location.reload();
                })
            }
        } else {
            alert("먼저 로그인을 해주세요!")
        }
    }
})

// Gather button behavior
const gatheringButtons = document.querySelectorAll(".gather")

$.ajax({
    type: "GET",
    url: "/gathering_check",
    data: {},
    success: function(response) {
        if (response["result"] == "success") {
            for (let i = 0; i < gatheringButtons.length; i++) {
                gatheringButtons[i].addEventListener("click", function() {
                    document.querySelector(".gathering-form").className += " is-active"
                    resName = this.parentElement.parentElement.querySelector('.title').innerHTML
                    document.querySelector(".restaurant-name").value = resName
                })
            }

            document.querySelector(".gathering-form-close").addEventListener("click", function() {
                document.querySelector(".gathering-form").classList.remove("is-active")
            });
        } else {
            alert("먼저 로그인을 해주세요!")
        }
    }
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
                alert("다시 시도해주세요!")
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
        success: function(response) {
            if (response["result"] == "success") {
                alert("로그인 성공!");
                window.location.reload();
                // Save jwt token
                // token = token from server
                // document.cookie = "token=" + token

                // remove login and signup buttons
                // append logout button
                // add event to logout button
                    // delete token from cookie
            } else {
                alert("아이디나 비밀번호가 틀렸습니다.")
            }
        }
    })
})

// Gathering form behavior
document.querySelector(".make-gather").addEventListener("click", function() {

    if (!document.querySelector(".meeting-time").value) {
        alert("모임 시간을 입력해주세요!")
    } else if (!document.querySelector(".participants-number").value) {
        alert("인원 수를 입력해주세요!")
    } else if (document.querySelector(".meeting-time").value > 60) {
        alert("모임 시간은 최대 60분까지 설정할 수 있습니다.")
    }

    let numberOfParticipants_temp = document.querySelector(".participants-number").value
    let meetingTime_temp = document.querySelector(".meeting-time").value
    let restaurantId_temp = document.querySelector(".restaurant-name").value
    //add user name to post data

    $.ajax({
        type: "POST",
        url: "/create_event",
        data: { restaurantId: restaurantId_temp, numberOfParticipants: numberOfParticipants_temp, meetingTime: meetingTime_temp },
        success: function(response){
            if (response["result"] == "success") {
                alert("모임이 만들어 졌습니다!");
                window.location.reload();
            } else {
                alert("다시 시도해주세요!")
            }
        }
    })
})



