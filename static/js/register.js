document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // 기본 폼 제출 동작 방지

        // 폼 데이터 가져오기
        const user_id = document.getElementById("user_id").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // 서버로 데이터 전송
        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id, username, password }),
            });

            const data = await response.json();

            if (data.result == 0) {
                showMessage("모든 필드를 입력하세요.", "red");
            } else if (data.result == 1) {
                alert("회원가입 성공! 로그인 페이지로 이동합니다.");
                window.location.href = "/login";
            } else if (data.result == 2) {
                showMessage("이미 존재하는 아이디입니다. 다른 아이디를 사용하세요.", "red");
            } else {
                showMessage("알 수 없는 오류가 발생했습니다.", "red");
            }
        } catch (error) {
            console.error("Error:", error);
            showMessage("서버 오류가 발생했습니다.", "red");
        }
    });

    // 메시지 표시 함수
    function showMessage(message, color) {
        messageDiv.textContent = message;
        messageDiv.style.color = color;
    }
});
