# backend/chat/execute.py
import os, sys, time, tempfile, subprocess, traceback

#local 경로
#GCC = r"C:\winlibs\mingw64\bin\gcc.exe"

GCC = "/usr/bin/gcc"

TIMEOUT_SEC = 2
MAX_OUT = 16 * 1024

def _cut(s: str) -> str:
    if not s:
        return ""
    return s if len(s) <= MAX_OUT else s[:MAX_OUT] + "\n...[truncated]"

def _decode_bytes(b: bytes) -> str:
    if b is None:
        return ""
    for enc in ("utf-8", "cp949", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            continue
    # 마지막 안전망
    return b.decode("utf-8", errors="replace")

def execute_c(code: str) -> dict:
    if not os.path.exists(GCC):
        return {"stdout":"", "stderr":f"gcc not found at: {GCC}", "exit_code":127, "time_ms":0}

    # Windows에서 콘솔창이 뜨지 않도록
    creationflags = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW

    try:
        with tempfile.TemporaryDirectory() as tmp:
            c_path  = os.path.join(tmp, "main.c")
            exe_path = os.path.join(tmp, "a.exe" if os.name == "nt" else "a.out")

            with open(c_path, "w", encoding="utf-8") as f:
                f.write(code)

            # 1) 컴파일 (raw bytes 캡처)
            comp = subprocess.run(
                [GCC, c_path, "-o", exe_path, "-std=c11", "-O0", "-Wall"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                cwd=tmp, creationflags=creationflags
            )
            if comp.returncode != 0:
                return {
                    "stdout": "",
                    "stderr": _cut(_decode_bytes(comp.stderr)),
                    "exit_code": comp.returncode,
                    "time_ms": 0,
                }

            # 2) 실행 (raw bytes 캡처)
            start = time.perf_counter()
            run = subprocess.run(
                [exe_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=TIMEOUT_SEC, cwd=tmp, creationflags=creationflags
            )
            ms = int((time.perf_counter() - start) * 1000)

            stdout_text = _cut(_decode_bytes(run.stdout))
            stderr_text = _cut(_decode_bytes(run.stderr))

            return {
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": run.returncode,
                "time_ms": ms,
            }

    except subprocess.TimeoutExpired:
        return {"stdout":"", "stderr":f"Timeout ({TIMEOUT_SEC}s)", "exit_code":124, "time_ms":TIMEOUT_SEC*1000}
    except Exception as e:
        return {"stdout":"", "stderr":f"Unhandled error: {type(e).__name__}: {e}\n{traceback.format_exc()}",
                "exit_code":1, "time_ms":0}
