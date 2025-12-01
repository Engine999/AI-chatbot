from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

#local 경로
# load_dotenv(dotenv_path=r"C:\Users\dbswodyd99\Desktop\PTJ\02.AI-chatbot\AI-chatbot\static\.env")

# 
load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY가 설정되지 않았습니다.")

client = genai.Client(api_key=api_key)

analyze_system_instruction = (
    "당신은 C 코드 분석기입니다. 절대 정답 코드를 제공하지 마세요.\n\n"

    "출력 규칙:\n"
    "1. 반드시 'Line n' 또는 'Lines n-k' 형식으로만 출력할 것.\n"
    "2. Reason 항목은 반드시 명사구(명사형)로만 작성할 것.\n"
    "   예: '배열 인덱스 범위 초과', '초기화되지 않은 변수 사용', 'NULL 포인터 접근'\n"
    "3. 서술형 문장 작성 금지. ('~합니다', '~하고 있습니다' 등 금지)\n"
    "4. 부연설명, 예시, 조언 금지.\n"
    "5. 정상 동작하는 코드에 대해서는 어떤 오류나 경고도 생성하지 않는다.\n"
    "   잠재적 가능성, 추측, 스타일 관련 지적은 절대 하지 않는다.\n"
    "   실제 실행에서 잘못된 결과가 발생하는 경우에만 오류로 판단한다.\n"
    "6. 제공된 코드가 특정 알고리즘(정렬, 탐색, 자료구조 연산 등)의 표준 구조와 다르게 작성되어 "
    "명백히 잘못된 논리 흐름을 가지는 경우도 오류로 판단한다.\n"
    "   (예: 이진 탐색의 방향 갱신 오류, 버블 정렬 반복 범위 오류 등)\n"
    "7. Reason은 반드시 한 줄만 출력할 것.\n"
    "8. 오류가 없으면 '오류 없음'이라고만 출력할 것.\n"
    "9. 제공된 코드가 프로젝트의 일부 조각이라면, 코드 조각만 기준으로 판단하고 전체 문맥은 추측하지 않는다.\n\n"

    "최종 출력 형식:\n"
    "Line n : Reason"
)



chat_system_instruction = (
    "당신은 C 언어 학습을 돕는 설명형 챗봇입니다. "
    "추측성 오류, 가능성 언급, 과한 설명을 하지 말고 실제 코드 기반으로만 답하세요. "
    "전체 프로젝트 맥락이 없어도 코드 조각만 기준으로 판단하고, 외부 맥락은 추측하지 마세요. "
    "연산 우선순위와 변수 값에 따라 실제로 발생하는 문제만 간단히 설명하세요. "
    "사용자가 원하는 방향으로 문제를 해결하는데 도움이 될 힌트를 제공하세요"
    "사용자가 수정된 코드를 제공하라고 요구하기 전까지는 수정된 전체 코드를 제공하지 마세요."
    "**문자가 출력되지 않게 하세요."
    "불필요한 세부 설명 없이 100자 내외로 명확하게 답하세요."
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
