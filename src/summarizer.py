import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


def summarize_article(article):
    if not GEMINI_API_KEY:
        print("[summarizer] GEMINI_API_KEY not set, skipping")
        return None

    title = article.get("title", "")
    content = article.get("summary", "")[:1000]

    prompt = (
        f"Artikel berita Bitcoin berikut relevan karena berkaitan dengan "
        f"metrik on-chain, ETF, makroekonomi, atau regulasi.\n\n"
        f"Judul: {title}\n"
        f"Konten: {content}\n\n"
        f"Berikan analisis singkat dalam 2-3 kalimat bahasa Indonesia:\n"
        f"- Apa inti berita ini?\n"
        f"- Mengapa ini penting bagi investor Bitcoin?"
    )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        result = response.text.strip()
        print(f"[summarizer] Summary generated for: {title[:60]}")
        return result
    except Exception as e:
        print(f"[summarizer] ERROR: {e}")
        return None
