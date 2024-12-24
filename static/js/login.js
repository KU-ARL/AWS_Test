document.addEventListener("DOMContentLoaded", () => {
    // 로그인 폼
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // 기본 폼 제출 동작 방지

        const formData = new FormData(loginForm);

        try {
            const response = await fetch("/login", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            if (data.result == 1) {
                alert("로그인 성공! 메인 페이지로 이동합니다.");
                window.location.href = "/upload"; 
            } else {
                alert("로그인 실패! 아이디 또는 비밀번호를 확인해주세요.");
            }
        } catch (error) {
            console.error("로그인 요청 중 오류 발생:", error);
            alert("서버와의 통신 중 문제가 발생했습니다.");
        }
    });
});
