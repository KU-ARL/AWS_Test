document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/upload", { method: "GET" });

        if (!response.ok) {
            const data = await response.json();
            switch (data.result) {
                case 0:
                    alert("세션이 없습니다! 로그인 후 다시 시도해주세요.");
                    window.location.href = "/login"; // 로그인 페이지로 리다이렉트
                    break;
                case 2:
                    alert("세션이 만료되었습니다. 다시 로그인해주세요.");
                    window.location.href = "/login"; // 로그인 페이지로 리다이렉트
                    break;
                default:
                    alert("알 수 없는 오류가 발생했습니다.");
            }
        }
    } catch (error) {
        console.error("Error during session validation:", error);
        alert("서버 요청 중 오류가 발생했습니다.");
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form[action='/upload']");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // 폼 기본 제출 동작 방지

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
            } else {
                alert("알 수 없는 오류가 발생했습니다.");
            }

        } catch (error) {
            console.error("Error:", error);
            alert("서버 요청 중 오류가 발생했습니다.");
        }
    });
});
