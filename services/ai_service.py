# services/ai_service.py

from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from config import OPENAI_API_KEY

def answer_question(df, question):
    llm = OpenAI(api_token=OPENAI_API_KEY)
    sdf = SmartDataframe(df, config={"llm": llm})
    return sdf.chat(question)
