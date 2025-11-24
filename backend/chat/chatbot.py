from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv(dotenv_path=r"C:\Users\dbswodyd99\Desktop\PTJ\02.AI-chatbot\AI-chatbot\static\.env")
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY가 설정되지 않았습니다.")

client = genai.Client(api_key=api_key)

analyze_system_instruction = (
    "당신은 C 코드 분석기입니다. 절대 정답 코드를 제공하지 마세요. "
    "반드시 아래 형식을 유지해 답변하세요.\n\n"
    "출력 규칙:\n"
    "1. 'Line n' 또는 'Lines n-k' 형식으로만 출력.\n"
    "2. Reason 항목은 반드시 명사구(명사형)로만 작성.\n"
    "   예: '배열 인덱스 범위 초과', '초기화되지 않은 변수 사용', 'NULL 포인터 접근'\n"
    "3. 절대로 서술형 문장(예: '~하고 있습니다', '~입니다', '~해야 합니다')을 작성하지 말 것.\n"
    "4. 부연설명 금지, 예시 금지, 조언 금지.\n"
    "5.확장성,유지보수성은 고려하지 말 것"
    "6. Reason은 한 줄만.\n\n"
    "최종 출력 형식:\n"
    "Line n : Reason <명사구>"
    "7.오류가 없으면 오류 없음 이라고 출력할 것"
)


chat_system_instruction = (
    "당신은 C 언어 학습을 돕는 설명형 챗봇입니다. "
    "정답 코드를 그대로 제공하지 말고, 단계별 이해를 돕고 힌트를 제시하세요."
    "사용자가 묻는 내용을 쉽게 풀어서 설명하세요. 하지만 비유 말고 알기 쉬우면서도 학술적이고 기술적이며 논리적으로 설명하세요."
    "100자 내외로 답변해주세요."
)

def gemini_analyze(code_str: str):
    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=code_str,
        config=types.GenerateContentConfig(
            system_instruction=analyze_system_instruction,
            temperature=0.3,
            max_output_tokens=50,
        ),
    )
    return resp.text

def gemini_chat(prompt: str):
    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=chat_system_instruction,
            temperature=0.3,
            max_output_tokens=300,
        ),
    )
    return resp.text
