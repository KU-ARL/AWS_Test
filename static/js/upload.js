document.addEventListener("DOMContentLoaded", async () => {
    validation();
});


document.addEventListener("DOMContentLoaded", async () => {
    
    // 업로드 버튼
    const form = document.querySelector("form[action='/upload']");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // 폼 기본 제출 동작 방지

        const isInvalidSession = await validation(); // 로그인 했는지 먼저 확인
        if (isInvalidSession) return; // 유효하지 않은 세션이면 중단

        const formData = new FormData(form);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if ( data.result == 0 ) {
                alert("이미지 파일이 선택되지 않았습니다.");
            } else if (data.result == 1) {
                alert("파일명이 없습니다. 파일을 다시 선택하세요.");
            } else if (data.result == 2) {
                alert(`Predicted Artist: ${data.artist}, Confidence: ${data.confidence}`);
            } else if (data.result == 3) {
                alert("JPG 형식의 파일만 업로드 가능합니다.");
            } else if (data.result == 4) {
                console.log("로그인 세션 만료");
            } else {
                alert("알 수 없는 오류가 발생했습니다.");
            }

        } catch (error) {
            console.error("Error:", error);
            alert("서버 요청 중 오류가 발생했습니다.");
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {

    // 로그아웃 버튼
    const logoutButton = document.getElementById("logout-button");

    logoutButton.addEventListener("click", async () => {
        try {
            const response = await fetch("/logout", { method: "GET" });

            const data = await response.json();

            if ( data.result == 0 ) {
                alert("로그아웃 성공! 로그인 페이지로 이동합니다.");
            } else if (data.result == 1) {
                alert("넌 이미 세션에도 없는 녀석이다.");
            } else if (data.result == 2) {
                alert("쿠키도 없이 어떻게 들어왔디야?");
            } else {
                alert("알 수 없는 오류가 발생했습니다.");
            }

            // 항상 로그인 페이지로 리다이렉트
            window.location.href = "/login";
        } catch (error) {
            console.error("Error during logout:", error);
            alert("서버 요청 중 오류가 발생했습니다.");
        }
    });
});


async function validation() {
    try {
        const response = await fetch("/validation", { method: "GET" });
        const data = await response.json();

        if ( data.result == 0 ) {
            alert("로그인 세션이 없습니다. 로그인 페이지로 이동합니다.");
            window.location.href = "/login";
            return 1;
        } else if (data.result == 1) { // 잘 로그인 되어있어서 그냥 패스
            return 0; 
        } else if (data.result == 2) {
            alert("세션이 만료되었습니다. 다시 로그인해주세요.");
            window.location.href = "/login";
            return 1;
        } else {
            alert("알 수 없는 오류가 발생했습니다.");
            return 1;
        }

    } catch (error) {
        console.error("유효성 검사 중 오류 발생:", error);
        alert("서버 요청 중 문제가 발생했습니다.");
    }
}