$(document).ready(function ($) {
    firebase.auth().onAuthStateChanged(function (user) {
        console.log("user:", user)
        var cu = window.location.href;
        // current url : 현재 주소 출력 
        var n1 = cu.indexOf("auth/login");
        // http://127.0.0.1:5500/public/auth/login/  => n1 = 29
        // http://127.0.0.1:5500/public  => n1 = -1
        if (user) {
            // 로그인 상태 
            if (n1 > 1) {
                // 로그인 상태에서 로그인 페이지로 갈 경우 
                window.open("../../", "_self", false);
            } else {
                // 로그인 상태에서 홈화면에 들어갈 경우
                console.log("home", user);
                $("#lblemail").text(user.email);
            }
        } else {
            $(".auth").css("display", "none")



            // 로그아웃 상태에서 홈화면에 들어올 경우 
            if (n1 < 1) {
                $("#state_login").text("로그인");
                $("#state_logout").css("display", "none");
            }
        }
    })
})