# NLP Techniques Used in AlphaCross

## Project

**AlphaCross – AI Powered Stock Market Analysis & Decision Support Platform**

---

# Overview

AlphaCross integrates **Natural Language Processing (NLP)** to transform raw financial news articles into meaningful investment insights.

Instead of displaying news directly, the system performs:

- News Retrieval
- Text Preprocessing
- Duplicate Removal
- Prompt Engineering
- Large Language Model based Financial NLP
- Sentiment Analysis
- Summarization
- Risk Extraction
- Impact Analysis

These NLP capabilities allow investors to understand the market context behind technical signals.

---

# NLP Pipeline

```
NewsData API
        │
        ▼
Raw Financial Articles
        │
        ▼
Text Cleaning
        │
        ▼
Duplicate Removal
        │
        ▼
Prompt Construction
        │
        ▼
Groq Llama 3.3 70B
        │
        ▼
Financial NLP
        │
        ├── Sentiment Classification
        ├── Summarization
        ├── Risk Extraction
        └── Impact Analysis
```

---

# NLP Concepts Used

## 1. Information Retrieval (IR)

The first NLP stage involves retrieving relevant financial news.

Source:

- NewsData.io API

The system searches using company names (e.g., Infosys, Reliance, ICICI Bank) to collect recent financial articles.

Output:

- Title
- Summary
- Source
- URL
- Publication Date

---

## 2. Text Preprocessing

Before sending data to the LLM, the news undergoes preprocessing.

Techniques used:

- Removing duplicate headlines
- Removing empty articles
- Cleaning unwanted characters
- Formatting structured text
- Combining multiple articles

Example:

Input

Headline:
Infosys signs cloud partnership.

Summary:
Infosys will modernize...

↓

Converted into structured prompt format.

---

## 3. Named Entity Recognition (NER)

Although no standalone NER library (SpaCy/BERT) is used, the LLM performs implicit entity recognition.

It automatically identifies:

- Company Names
- Organizations
- Products
- Business Events
- Countries
- CEOs

Example

"Infosys Finacle selected by Investec"

↓

Entities detected

Company

- Infosys

Product

- Finacle

Organization

- Investec

---

## 4. Prompt Engineering

Instead of asking the model

"Summarize this"

the project uses structured prompts.

Example

Headline

Summary

Source

for every article.

The model is instructed to return

```
SENTIMENT:

CONFIDENCE:

SUMMARY:

RISKS:

IMPACT:
```

This ensures deterministic and structured responses.

---

## 5. Large Language Model (LLM)

Model Used

Groq

Model

Llama 3.3 70B Versatile

Role

Acts as the NLP engine.

Tasks performed

- Semantic Understanding
- Financial Reasoning
- Context Interpretation
- Summarization
- Risk Analysis

---

## 6. Abstractive Summarization

Instead of copying news sentences,

the LLM generates a new concise explanation.

Input

Multiple financial articles

↓

Output

A 3–4 sentence investor-friendly summary.

This is known as

Abstractive Text Summarization.

---

## 7. Financial Sentiment Analysis

The model classifies news sentiment into

- Bullish
- Bearish
- Neutral

Unlike keyword matching,

the LLM understands context.

Example

"Company wins ₹2000 crore defence contract"

↓

Bullish

Example

"Quarterly profit drops despite higher revenue"

↓

Bearish

---

## 8. Confidence Scoring

The model also predicts confidence.

Example

Bullish (82%)

This indicates how strongly the available news supports the predicted sentiment.

---

## 9. Information Extraction

The LLM extracts important business risks from news articles.

Example

Input

Infosys selected for banking modernization.

Output

- Project execution risk
- Integration challenges
- Regulatory uncertainty

This converts unstructured text into structured knowledge.

---

## 10. Contextual Impact Analysis

The system compares

Technical Analysis

+

Financial News

to determine whether news supports or contradicts the technical trend.

Example

Technical Trend

Bullish

News Sentiment

Bearish

↓

Overall Impact

Possible short-term reversal.

This combines NLP with quantitative analysis.

---

# NLP Techniques Summary

| NLP Technique | Used | Purpose |
|--------------|------|---------|
| Information Retrieval | ✅ | Fetch financial news |
| Text Preprocessing | ✅ | Clean and structure articles |
| Duplicate Removal | ✅ | Remove repeated headlines |
| Prompt Engineering | ✅ | Structured LLM interaction |
| Named Entity Recognition (Implicit) | ✅ | Detect companies and business entities |
| Semantic Understanding | ✅ | Understand financial context |
| Financial Sentiment Analysis | ✅ | Bullish / Bearish / Neutral prediction |
| Abstractive Summarization | ✅ | Generate concise investor summaries |
| Information Extraction | ✅ | Extract business risks |
| Contextual Reasoning | ✅ | Compare news with technical trend |
| Large Language Model | ✅ | Core NLP engine |

---

# NLP Libraries & Technologies

Programming Language

- Python

Libraries

- Requests
- Regular Expressions (re)
- Pandas

LLM

- Groq API

Foundation Model

- Llama 3.3 70B Versatile

News Source

- NewsData.io

---

# Overall NLP Workflow

```
NewsData API
      │
      ▼
Financial Articles
      │
      ▼
Cleaning
      │
      ▼
Deduplication
      │
      ▼
Prompt Engineering
      │
      ▼
Groq Llama 3.3
      │
      ▼
Natural Language Processing
      │
      ├── Sentiment Analysis
      ├── Summarization
      ├── Risk Extraction
      ├── Entity Recognition
      └── Impact Analysis
      │
      ▼
Dashboard Visualization
```

---

# Learning Outcomes

Through this project, the following NLP concepts were implemented:

- Information Retrieval
- Text Preprocessing
- Prompt Engineering
- Large Language Models
- Financial NLP
- Sentiment Analysis
- Abstractive Summarization
- Information Extraction
- Contextual Semantic Analysis
- Explainable AI Integration with NLP