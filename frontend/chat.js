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
    printf("Hello C!\\n");
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
function setExecOutput(text) {
  const out = document.getElementById("execResult");
  if (out) out.textContent = text;
}
function getCodeSafe() {
  if (!monacoReady || !editor) return null;
  return editor.getValue();
}

/* =======================
   AI 채팅 유틸
   ======================= */
const chatWindow = document.getElementById("chatWindow");
const chatInput  = document.getElementById("chatInput");
const chatSendBtn = document.getElementById("chatSendBtn");

// 간단한 메모리(최근 몇 턴)
const history = [];

function appendChat(role, text) {
  const wrap = document.createElement("div");
  wrap.className = "msg " + role; // .msg.user / .msg.assistant 등 CSS로 꾸미세요.
  wrap.textContent = text;
  chatWindow.appendChild(wrap);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

/* =======================
   코드 실행 → 결과 표시 → AI 분석 자동 호출
   ======================= */
document.addEventListener("DOMContentLoaded", () => {
  const runBtn = document.getElementById("runBtn");
  if (!runBtn) return;

  runBtn.addEventListener("click", async () => {
    const code = getCodeSafe();
    if (code === null) {
      setExecOutput("Editor is still loading. 잠시 후 다시 시도하세요.");
      return;
    }
    if (!code.trim()) {
      setExecOutput("코드가 비어 있습니다.");
      return;
    }

    // 실행 호출
    runBtn.disabled = true;
    runBtn.textContent = "Running...";
    setExecOutput("Running...");

    try {
      const res = await fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      if (!res.ok) {
        const text = await res.text();
        setExecOutput(`HTTP ${res.status}\n${text}`);
        return;
      }

      const data = await res.json();
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
      setExecOutput(lines.join("\n"));

      // === 실행 결과 이후 자동 분석 호출 ===
      appendChat("system", "코드 분석을 시작합니다…");
      const analyzeRes = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const analyzeJson = await analyzeRes.json();
      if (analyzeRes.ok && analyzeJson?.result) {
        appendChat("assistant", analyzeJson.result);
        history.push({ role: "assistant", content: analyzeJson.result });
      } else {
        appendChat("assistant", `분석 오류: ${analyzeJson?.detail ?? "Unknown error"}`);
      }
    } catch (err) {
      setExecOutput("요청 실패: " + err);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = "execute";
    }
  });
});

/* =======================
   채팅: 사용자가 질문 → /chat
   ======================= */
async function sendChat() {
  const message = (chatInput?.value ?? "").trim();
  if (!message) return;
  const code = getCodeSafe() ?? "";

  appendChat("user", message);
  history.push({ role: "user", content: message });
  chatInput.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        code,
        history,
      }),
    });
    const json = await res.json();
    if (res.ok && json?.result) {
      appendChat("assistant", json.result);
      history.push({ role: "assistant", content: json.result });
    } else {
      appendChat("assistant", `오류: ${json?.detail ?? "Unknown error"}`);
    }
  } catch (e) {
    appendChat("assistant", "네트워크 오류: " + String(e));
  }
}

if (chatSendBtn) {
  chatSendBtn.addEventListener("click", sendChat);
}
if (chatInput) {
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      sendChat();
    }
  });
}
