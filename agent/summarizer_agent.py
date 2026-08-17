# agent/summarizer_agent.py

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import GROQ_API_KEY, GROQ_MODEL, USER_PROFILE


def build_summarizer_chain():
    llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)

    prompt = ChatPromptTemplate.from_template("""
أنت مساعد AI شخصي لـ {name}.

معلومات عنه:
- خلفيته: {background}
- مهاراته: {skills}
- مشروعه الحالي: {current_project}
- هدفه: {goal}
- مساره: {learning_path}

المطلوب منك لهذا الخبر:

**الخبر:**
{title}

**المحتوى:**
{content}

أجب بهذا الشكل بالضبط — بالعربي العراقي:

ملخص: [ملخص الخبر بـ 2-3 جمل]

أهميته ليك: [اشرح لمرتضى بالعراقي السوالفي شنو يعني هذا الخبر ليه هو شخصياً، 
كيف يربط بمشروعه أو مساره أو مهاراته، وشنو يقدر يسوي بيه]
""")

    return prompt | llm | StrOutputParser()


def summarizer_agent(state: dict) -> dict:
    articles = state.get("filtered_articles", [])
    print(f"=== Summarizer استلم: {len(articles)} مقالة ===") 
    if not articles:
        return {**state, "summarized_articles": []}

    chain = build_summarizer_chain()
    summarized = []

    for article in articles:
        try:
            response = chain.invoke({
                "name": USER_PROFILE["name"],
                "background": USER_PROFILE["background"],
                "skills": ", ".join(USER_PROFILE["skills"]),
                "current_project": USER_PROFILE["current_project"],
                "goal": USER_PROFILE["goal"],
                "learning_path": USER_PROFILE["learning_path"],
                "title": article.get("title", ""),
                "content": article.get("content", "")[:1000],
            })
            
            summary, personal = parse_response(response)

            summarized.append({
                **article,
                "summary": summary,
                "personal_insight": personal
            })

        except Exception as e:
            print(f"❌ خطأ في تلخيص: {article.get('title')} — {e}")

    return {**state, "summarized_articles": summarized}


def parse_response(response: str) -> tuple:
    summary = ""
    personal = ""

    lines = response.strip().split("\n")

    current = None
    for line in lines:
        clean = line.strip().replace("**", "").replace("*", "")
        
        if clean.startswith("ملخص:"):
            current = "summary"
            summary = clean.replace("ملخص:", "").strip()
        elif clean.startswith("أهميته ليك:"):
            current = "personal"
            personal = clean.replace("أهميته ليك:", "").strip()
        elif current == "summary" and clean:
            summary += " " + clean
        elif current == "personal" and clean:
            personal += " " + clean

    return summary.strip(), personal.strip()