let editor;
let monacoReady = false;

/* =======================
   Monaco Editor 초기화
   ======================= */
(function initMonaco() {
  if (typeof require === "undefined") {
    console.error("Monaco loader not loaded");
    return;
  }

  require.config({
    paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs" },
  });

  require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create(document.getElementById("editor"), {
      value: `#include <stdio.h>

int main(void) {
  
    // your code...
    printf("Hello C!");
    
    return 0;
}
`,
      language: "c",
      theme: "vs-dark",
      automaticLayout: true,
      fontSize: 15,
      minimap: { enabled: false },
    });
    monacoReady = true;
  });
})();

/* =======================
   유틸리티
   ======================= */
function setOutput(text) {
  const out = document.getElementById("execResult");
  if (out) out.textContent = text;
}

function getCodeSafe() {
  if (!monacoReady || !editor) return null;
  return editor.getValue();
}

/* =======================
   실행 버튼 핸들러
   ======================= */
document.addEventListener("DOMContentLoaded", () => {
  const runBtn = document.getElementById("runBtn");
  const out = document.getElementById("execResult");

  if (!runBtn || !out) {
    console.error("Required elements not found: #runBtn or #execResult");
    return;
  }

  runBtn.addEventListener("click", async () => {
    // Monaco 준비 전 클릭 방지
    const code = getCodeSafe();
    if (code === null) {
      setOutput("Editor is still loading. 잠시 후 다시 시도하세요.");
      return;
    }

    // 빈 코드 방지(선택)
    if (!code.trim()) {
      setOutput("코드가 비어 있습니다.");
      return;
    }

    // 버튼 잠금
    runBtn.disabled = true;
    runBtn.textContent = "Running...";
    setOutput("Running...");

    try {
      const res = await fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      // HTTP 에러 본문도 보여주기
      if (!res.ok) {
        const text = await res.text();
        setOutput(`HTTP ${res.status}\n${text}`);
        return;
      }

      // JSON 파싱
      let data;
      try {
        data = await res.json();
      } catch (e) {
        setOutput("응답 파싱 실패(Invalid JSON).");
        return;
      }

      // 표준 출력/에러 정리
      const lines = [];
      lines.push(`exit: ${data.exit_code}    time: ${data.time_ms}ms`, "");
      if (data.stdout && data.stdout.length) {
        lines.push("stdout:", data.stdout, "");
      }
      if (data.stderr && data.stderr.length) {
        lines.push("stderr:", data.stderr);
      }
      if ((!data.stdout || !data.stdout.length) && (!data.stderr || !data.stderr.length)) {
        lines.push("(no output)");
      }

      setOutput(lines.join("\n"));
    } catch (err) {
      setOutput("요청 실패: " + err);
    } finally {
      // 버튼 해제
      runBtn.disabled = false;
      runBtn.textContent = "execute";
    }
  });
});
