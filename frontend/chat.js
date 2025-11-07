let editor;

(function initMonaco() {
  // CDN 로더가 먼저 로드되므로 require 사용 가능
  // 경로는 loader.min.js의 require.config 규격에 맞게 지정
  if (typeof require === "undefined") {
    console.error("Monaco loader가 아직 로드되지 않았습니다.");
    return;
  }

  require.config({
    paths: {
      vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs",
    },
  });

  require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create(document.getElementById("editor"), {
      value: `#include <stdio.h>

int main() {
    printf("Hello world");
    return 0;
}
`,
      language: "c",
      theme: "vs-dark",
      automaticLayout: true,
      fontSize: 15,
      minimap: { enabled: false },
    });

    // 필요 시 다른 파일에서 사용할 수 있도록 전역 getter 노출
    window.getCode = () => (editor ? editor.getValue() : "");
  });
})();
