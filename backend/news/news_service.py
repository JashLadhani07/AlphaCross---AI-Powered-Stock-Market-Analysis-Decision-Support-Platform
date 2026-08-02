"""
News Intelligence module for AlphaCross.

Pipeline:
  GNews API (headlines) -> clean/dedupe -> Groq LLM
  -> structured summary + sentiment + risks + impact

Requires (optional, degrades gracefully if unset):
  GROQ_API_KEY    - https://console.groq.com

If NEWSDATA_API_KEY is missing: returns an "unavailable" payload (no crash).
If GROQ_API_KEY is missing: returns headlines with a simple rule-based
fallback summary instead of an AI-generated one.
"""

import os
import re
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

NEWSDATA_URL = "https://newsdata.io/api/1/news"
GROQ_MODEL = "llama-3.3-70b-versatile"

BASE_DIR = Path(__file__).resolve().parents[2]

NSE500_CSV = BASE_DIR / "backend" / "data" / "nifty500.csv"

try:
    COMPANY_DF = pd.read_csv(NSE500_CSV)
except Exception as e:
    print(e)
    COMPANY_DF = pd.DataFrame()


def get_company_name(symbol: str) -> str:
    """
    Convert NSE ticker -> Company name
    Example:
        INFY -> Infosys Ltd.
        TCS -> Tata Consultancy Services Ltd.
    """

    if COMPANY_DF.empty:
        return symbol

    row = COMPANY_DF[
        COMPANY_DF["Symbol"].str.upper() == symbol.upper()
    ]

    if row.empty:
        return symbol

    return row.iloc[0]["Company Name"]


# ---------------------------------------------------------------------------
# 1. Fetch
# ---------------------------------------------------------------------------
def fetch_headlines(symbol: str, max_articles: int = 10) -> List[Dict[str, str]]:

    api_key = os.getenv("NEWSDATA_API_KEY")

    if not api_key:
        return []

    company = get_company_name(symbol)
    company = (
        company.replace("Limited", "")
           .replace("Ltd.", "")
           .replace("Ltd", "")
           .replace("Corporation", "")
           .replace("Industries", "")
           .strip()
)

    params = {
        "apikey": api_key,
        "qInTitle": company,
        "country": "in",
        "language": "en",
        #"category": "business",
    }

    try:
        resp = requests.get(NEWSDATA_URL, params=params, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        articles = data.get("results", [])

        return [
            {
                "title": article.get("title", "").strip(),
                "url": article.get("link", ""),
                "source": article.get("source_name", "Unknown"),
                "published_at": article.get("pubDate", ""),
                "summary": article.get("description", "").strip(),
            }
            for article in articles[:max_articles]
            if article.get("title")
        ]

    except Exception as e:
        print(f"[news_service] NewsData error for {symbol}: {e}")
        return []

# ---------------------------------------------------------------------------
# 2. Clean / dedupe (basic text preprocessing + semantic-ish similarity)
# ---------------------------------------------------------------------------
def _normalize(title: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", title.lower()).strip()


def dedupe_headlines(headlines: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove exact/near-duplicate headlines (simple token-overlap heuristic
    stands in for embedding-based clustering, keeping this dependency-free)."""
    seen_norms: List[str] = []
    unique: List[Dict[str, str]] = []

    for h in headlines:
        norm = _normalize(h["title"])
        if not norm:
            continue

        norm_tokens = set(norm.split())
        is_duplicate = False
        for existing in seen_norms:
            existing_tokens = set(existing.split())
            if not norm_tokens or not existing_tokens:
                continue
            overlap = len(norm_tokens & existing_tokens) / len(norm_tokens | existing_tokens)
            if overlap > 0.6:
                is_duplicate = True
                break

        if not is_duplicate:
            seen_norms.append(norm)
            unique.append(h)

    return unique


# ---------------------------------------------------------------------------
# 3. Groq summarization / sentiment / risk extraction
# ---------------------------------------------------------------------------
def _parse_groq_response(text: str) -> Dict[str, Any]:
    """Parse the structured Groq response into a dict."""
    result: Dict[str, Any] = {
        "sentiment": "Neutral",
        "confidence": 50,
        "summary": "",
        "risks": [],
        "impact": "",
    }

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        upper = line.upper()
        if upper.startswith("SENTIMENT:"):
            result["sentiment"] = line.split(":", 1)[1].strip()
        elif upper.startswith("CONFIDENCE:"):
            digits = "".join(c for c in line.split(":", 1)[1] if c.isdigit())
            if digits:
                result["confidence"] = min(100, int(digits))
        elif upper.startswith("SUMMARY:"):
            result["summary"] = line.split(":", 1)[1].strip()
        elif upper.startswith("RISKS:"):
            raw = line.split(":", 1)[1].strip()
            if raw.lower() not in ("none identified", "none", "n/a", ""):
                result["risks"] = [r.strip() for r in raw.split(";") if r.strip()]
        elif upper.startswith("IMPACT:"):
            result["impact"] = line.split(":", 1)[1].strip()

    return result


def analyze_with_groq(symbol: str, headlines: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    """Use Groq to summarize headlines, assign sentiment, and flag risks."""
    company = get_company_name(symbol)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    print("Groq key:", GROQ_API_KEY)
    print("Groq key:", GROQ_API_KEY)
    print("Headlines:", len(headlines))
    if not GROQ_API_KEY or not headlines:
        return None

    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        headlines_text = "" 
        for article in headlines:
            headlines_text += f"""
        Headline:
        {article['title']}
        Summary:
        {article.get('summary', 'No summary available.')}
        Source:
        {article['source']}
        ----------------------------------------
        """

        prompt=f"""You are a senior financial analyst. Company: {company} Ticker: {symbol}
        Below are the latest verified news articles. 
        {headlines_text}
        Analyze these articles and answer ONLY in the following format.
        SENTIMENT: Bullish / Bearish / Neutral
        CONFIDENCE: 0-100
        SUMMARY:
        Explain in 3-4 sentences what these news articles collectively mean for investors.
        RISKS:
        List important risks separated by semicolons.
        If none, write "None identified".
        IMPACT:
        Explain whether these news events support or contradict the current technical trend.
        """

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise, concise financial news analyst. "
                    "Never invent facts not present in the headlines. "
                    "Follow the requested output format exactly.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=350,
            temperature=0.4,
        )

        text = response.choices[0].message.content.strip()
        print("\n========== GROQ RESPONSE ==========\n")
        print(text)
        print("\n===================================\n")
        return _parse_groq_response(text)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None


def _fallback_analysis(headlines: List[Dict[str, str]]) -> Dict[str, Any]:
    """Used when Groq is unavailable - no AI summary, just raw counts."""
    return {
        "sentiment": "Neutral",
        "confidence": 0,
        "summary": (
            f"Found {len(headlines)} recent headline(s). Set GROQ_API_KEY to enable "
            "AI-generated summaries, sentiment, and risk analysis."
        ),
        "risks": [],
        "impact": "AI news analysis is not configured.",
    }


# ---------------------------------------------------------------------------
# 4. Public entrypoint
# ---------------------------------------------------------------------------
def get_news_intelligence(symbol: str) -> Dict[str, Any]:
    """Full pipeline: fetch -> dedupe -> summarize/sentiment/risks."""
    raw_headlines = fetch_headlines(symbol)
    headlines = dedupe_headlines(raw_headlines)

    if not headlines:
        return {
            "symbol": symbol,
            "available": False,
            "headlines": [],
            "sentiment": "Neutral",
            "confidence": 0,
            "summary": "",
            "risks": [],
            "impact": "",
            "message": (
                "No news available. Set GNEWS_API_KEY to enable News Intelligence."
                if not os.getenv("NEWSDATA_API_KEY")
                else "No recent articles found for this symbol."
            ),
        }

    analysis = analyze_with_groq(symbol, headlines) or _fallback_analysis(headlines)

    return {
        "symbol": symbol,
        "available": True,
        "headlines": headlines[:10],
        **analysis,
    }