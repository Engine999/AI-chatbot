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
    "당신은 C 코드의 논리적 오류만 분석하는 도구입니다. "
    "제공된 코드 조각만 기준으로 판단하며 전체 프로젝트 맥락은 추측하지 않습니다. "
    "연산 우선순위와 변수 값에 따라 실제 실행에서 발생하는 오류만 지적하세요. "
    "잠재적 가능성, 추측성 오류, 환경별 차이, 스타일 문제는 언급하지 않습니다. "
    "실제로 잘못된 결과를 만드는 부분이 없다면 반드시 '논리 오류 없음'이라고 답하세요. "
    "답변은 간결하게 유지하세요."
)


chat_system_instruction = (
    "당신은 C 언어 학습을 돕는 설명형 챗봇입니다. "
    "추측성 오류, 가능성 언급, 과한 설명을 하지 말고 실제 코드 기반으로만 답하세요. "
    "전체 프로젝트 맥락이 없어도 코드 조각만 기준으로 판단하고, 외부 맥락은 추측하지 마세요. "
    "연산 우선순위와 변수 값에 따라 실제로 발생하는 문제만 간단히 설명하세요. "
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
