# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# import os
# import sys

# load_dotenv(dotenv_path=r"C:\Users\dbswodyd99\Desktop\PTJ\02.AI-chatbot\AI-chatbot\static\.env")
# api_key = os.getenv("GOOGLE_API_KEY")


# client = genai.Client(api_key=api_key)
# system_instruction = (
#     "당신은 C 코드 학습용 리뷰어입니다. 절대 전체 정답 코드를 제공하지 마세요. "
#     "문제가 되는 Line을 명시하세요."
#     #"출력은 항상 JSON으로 반환하세요: {summary:{overall, categories:[...]}, hints:{L1, L2, L3}, checklist:[...]} "
#     #"카테고리는 syntax, memory-safety, logic, edge-cases, style, performance 중에서만 사용하세요."
# )

# user_input = sys.stdin.read()

# # 4) generate_content 호출 (system_instruction은 config로)
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents=user_input,
#     config=types.GenerateContentConfig(
#         system_instruction=system_instruction,
#         temperature=0.3,
#         max_output_tokens=512,
#     ),
# )

# print(f" : {response.text}")




