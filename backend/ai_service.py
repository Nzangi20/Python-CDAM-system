"""Centralized AI service layer for CDAM platform.

Provides a modular architecture with:
- GeminiProvider: wraps the google-generativeai SDK
- AIService: high-level orchestrator used by Flask routes
- Rate limiter: per-user in-memory token bucket
- Provider abstraction for future OpenAI/Anthropic support
"""

from __future__ import annotations

import os
import time
import threading
from abc import ABC, abstractmethod
from typing import Optional


# ---------------------------------------------------------------------------
# Provider abstraction
# ---------------------------------------------------------------------------

class BaseProvider(ABC):
    """Abstract base for AI providers (Gemini, OpenAI, Anthropic, etc.)."""

    @abstractmethod
    def generate(self, prompt: str, system_instruction: str = "", max_tokens: int = 2048) -> str:
        ...


class GeminiProvider(BaseProvider):
    """Google Gemini API provider using google-generativeai SDK."""

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self._model_name = model_name
        self._genai = genai

    def generate(self, prompt: str, system_instruction: str = "", max_tokens: int = 2048) -> str:
        try:
            model = self._genai.GenerativeModel(
                model_name=self._model_name,
                system_instruction=system_instruction or None,
                generation_config=self._genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                ),
            )
            response = model.generate_content(prompt)
            return response.text.strip() if response.text else "I couldn't generate a response. Please try again."
        except Exception as exc:
            return f"AI service encountered an error: {exc}"


class GroqProvider(BaseProvider):
    """Groq API provider using standard library HTTP requests or requests library."""

    def __init__(self, api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        self._api_key = api_key
        self._model_name = model_name

    def generate(self, prompt: str, system_instruction: str = "", max_tokens: int = 2048) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self._model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        try:
            import requests
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                res_json = response.json()
                choices = res_json.get("choices", [])
                if choices:
                    return choices[0]["message"]["content"].strip()
                return "Error: Empty choices list received from Groq API."
            return f"AI service (Groq) error: HTTP {response.status_code} - {response.text}"
        except ImportError:
            import urllib.request
            import json
            try:
                req = urllib.request.Request(
                    url, 
                    data=json.dumps(data).encode("utf-8"), 
                    headers=headers, 
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_body = response.read().decode("utf-8")
                    res_json = json.loads(res_body)
                    choices = res_json.get("choices", [])
                    if choices:
                        return choices[0]["message"]["content"].strip()
                return "Error: Empty response from Groq API."
            except Exception as exc:
                return f"AI service (Groq urllib) encountered an error: {exc}"
        except Exception as exc:
            return f"AI service (Groq) encountered an error: {exc}"


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

class RateLimiter:
    """Simple in-memory per-user rate limiter (token bucket)."""

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self._max = max_requests
        self._window = window_seconds
        self._buckets: dict[int, list[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        with self._lock:
            timestamps = self._buckets.get(user_id, [])
            # Prune expired entries
            timestamps = [t for t in timestamps if now - t < self._window]
            if len(timestamps) >= self._max:
                self._buckets[user_id] = timestamps
                return False
            timestamps.append(now)
            self._buckets[user_id] = timestamps
            return True


# ---------------------------------------------------------------------------
# System instructions
# ---------------------------------------------------------------------------

SYSTEM_INSTRUCTION = """You are an expert Python for Data Science tutor on the CDAM (Center for Data Analytics & Modelling) learning platform at Chuka University.

RULES:
- Be educational, encouraging, and precise.
- Use markdown formatting: headers, bold, code blocks, bullet lists.
- Provide practical Python examples when explaining concepts.
- Reference the session context (title, objectives, outcomes) naturally.
- NEVER provide answers to exam or quiz questions. If asked, politely decline.
- NEVER generate harmful, offensive, or irrelevant content.
- Keep responses concise but thorough (under 800 words unless generating questions/projects).
- When reviewing code, be educational — explain WHY, don't just rewrite.
- Format code examples with ```python code blocks.
"""


# ---------------------------------------------------------------------------
# AI Service
# ---------------------------------------------------------------------------

class AIService:
    """High-level AI service used by Flask routes."""

    def __init__(self, provider: BaseProvider | None = None):
        self._provider = provider
        self._rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

    @property
    def is_configured(self) -> bool:
        return self._provider is not None

    def check_rate_limit(self, user_id: int) -> bool:
        return self._rate_limiter.is_allowed(user_id)

    def _build_context(self, session) -> str:
        """Build session context string for prompts."""
        parts = [f"**Session Title:** {session.title}"]
        if session.objectives:
            parts.append(f"**Learning Objectives:**\n{session.objectives}")
        if session.expected_outcomes:
            parts.append(f"**Expected Outcomes:**\n{session.expected_outcomes}")
        if session.learning_notes:
            parts.append(f"**Learning Notes:**\n{session.learning_notes[:1500]}")
        if session.description:
            parts.append(f"**Description:** {session.description}")
        parts.append(f"**Difficulty:** {session.difficulty}")
        return "\n\n".join(parts)

    def _call(self, prompt: str, max_tokens: int = 2048) -> str:
        if not self._provider:
            return "AI service is not configured. Please add a GROQ_API_KEY or GEMINI_API_KEY to the environment."
        return self._provider.generate(prompt, system_instruction=SYSTEM_INSTRUCTION, max_tokens=max_tokens)

    # ----- Feature methods -----

    def explain_topic(self, session) -> str:
        context = self._build_context(session)
        prompt = f"""Explain the following lesson topic to a student who is learning Python for Data Science.

{context}

Please:
1. Simplify the concepts in beginner-friendly language
2. Provide 2-3 practical Python code examples
3. Highlight common mistakes students make
4. Explain real-world / industry applications of these concepts
5. Use analogies to make abstract concepts concrete"""
        return self._call(prompt)

    def explain_error(self, error_text: str, code: str, session) -> str:
        context = self._build_context(session)
        prompt = f"""A student encountered the following error while coding in the lesson:

{context}

**Student's Code:**
```python
{code[:2000]}
```

**Error Message:**
```
{error_text[:1000]}
```

Please:
1. Identify exactly what caused this error
2. Explain the error in simple, beginner-friendly language
3. Show the corrected code with ```python code blocks
4. Explain how to avoid this error in the future
5. If relevant, mention related Python concepts the student should review"""
        return self._call(prompt)

    def review_code(self, code: str, session) -> str:
        context = self._build_context(session)
        prompt = f"""Review the following student code for quality, best practices, and learning opportunities.

{context}

**Student's Code:**
```python
{code[:2000]}
```

Please provide an educational review:
1. **What's Good:** Highlight what the student did well
2. **Improvements:** Suggest specific improvements with explanations of WHY
3. **Best Practices:** Recommend Python/PEP-8 best practices relevant to their code
4. **Performance Tips:** Suggest any efficiency improvements (especially for Data Science)
5. **Learning Suggestion:** Recommend one concept they should explore next

Be encouraging and educational — explain reasoning, don't just rewrite the code."""
        return self._call(prompt)

    def generate_questions(self, session) -> str:
        context = self._build_context(session)
        prompt = f"""Generate practice questions based on this lesson for a Python Data Science student.

{context}

Create exactly:
1. **3 Multiple Choice Questions** — each with 4 options (A-D) and the correct answer marked
2. **2 Short Answer Questions** — requiring 2-3 sentence explanations
3. **2 Coding Exercises** — small practical tasks the student can solve in the code editor
4. **1 Challenge Task** — a harder problem that combines multiple concepts from this lesson

Format each section with clear headers and numbering. For MCQs, mark the correct answer."""
        return self._call(prompt, max_tokens=3000)

    def generate_project(self, session) -> str:
        context = self._build_context(session)
        prompt = f"""Generate a practical mini-project for a student based on this lesson.

{context}

Create a project that includes:
1. **Project Title** — a descriptive, engaging name
2. **Project Description** — 2-3 sentences explaining what the student will build
3. **Requirements** — bullet list of 5-7 specific features to implement
4. **Starter Code** — a Python code skeleton with comments indicating where students should add their code
5. **Expected Output** — describe what the finished project should produce
6. **Bonus Challenge** — an optional extension for advanced students

The project should be completable in 30-60 minutes and directly apply concepts from this lesson."""
        return self._call(prompt, max_tokens=3000)

    def summarize_session(self, session) -> str:
        context = self._build_context(session)
        prompt = f"""Generate a comprehensive study summary for this lesson.

{context}

Create a revision-ready summary with:
1. **Key Concepts** — the 5-7 most important ideas from this lesson
2. **Important Syntax & Functions** — essential Python commands/functions used, with brief descriptions
3. **Formulas / Patterns** — any key formulas, algorithms, or code patterns to memorize
4. **Common Pitfalls** — mistakes to watch out for
5. **Quick Reference Table** — a markdown table of the top functions/methods covered
6. **Exam Preparation Tips** — what to focus on for assessments related to this topic"""
        return self._call(prompt)

    def career_guidance(self, session) -> str:
        context = self._build_context(session)
        prompt = f"""Provide career guidance for a student learning this topic.

{context}

Cover:
1. **Career Paths** — which data careers use these skills (Data Analyst, Data Scientist, ML Engineer, AI Engineer)
2. **Industry Applications** — real companies and industries that rely on these skills
3. **Resume Tips** — how to showcase these skills on a resume or LinkedIn
4. **Portfolio Projects** — 2-3 project ideas to demonstrate mastery to employers
5. **Interview Preparation** — common interview questions related to this topic
6. **Next Steps** — what to learn next to advance in this career path"""
        return self._call(prompt)

    def analyze_dataset(self, file_content: str, filename: str, session) -> str:
        context = self._build_context(session)
        # Truncate large datasets to first ~50 rows for the prompt
        lines = file_content.split("\n")
        preview = "\n".join(lines[:51])
        total_rows = len(lines) - 1  # minus header

        prompt = f"""A student uploaded a dataset for analysis in the context of this lesson.

{context}

**Filename:** {filename}
**Total Rows:** ~{total_rows}
**Data Preview (first 50 rows):**
```
{preview[:3000]}
```

Please analyze this dataset and provide:
1. **Dataset Description** — what this data appears to represent
2. **Column Analysis** — describe each column (data type, meaning, sample values)
3. **Missing Values** — identify any missing/null patterns visible
4. **Cleaning Recommendations** — specific pandas code to clean this data
5. **Visualization Suggestions** — 2-3 chart types to explore this data, with matplotlib/seaborn code
6. **Machine Learning Approaches** — if applicable, suggest ML models suited to this dataset"""
        return self._call(prompt, max_tokens=3000)

    def chat(self, query: str, code: str, session) -> str:
        context = self._build_context(session)
        code_section = ""
        if code and code.strip():
            code_section = f"\n\n**Student's Current Code:**\n```python\n{code[:1500]}\n```"

        prompt = f"""A student asks the following question about this lesson:

{context}{code_section}

**Student's Question:** {query}

Provide a helpful, educational answer. If the question involves code, include Python examples. Stay focused on the lesson context."""
        return self._call(prompt)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

def create_ai_service() -> AIService:
    """Factory function to create the AI service with environment configuration."""
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    if groq_key:
        try:
            provider = GroqProvider(api_key=groq_key)
            return provider, AIService(provider=provider)
        except Exception:
            pass
            
    if gemini_key:
        try:
            provider = GeminiProvider(api_key=gemini_key)
            return provider, AIService(provider=provider)
        except Exception:
            pass
            
    return AIService(provider=None)


def get_ai_service() -> AIService:
    """Get or create the global AI service singleton."""
    global _ai_service_instance
    if _ai_service_instance is None:
        groq_key = os.environ.get("GROQ_API_KEY", "").strip()
        gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
        
        provider = None
        if groq_key:
            try:
                provider = GroqProvider(api_key=groq_key)
            except Exception:
                pass
        elif gemini_key:
            try:
                provider = GeminiProvider(api_key=gemini_key)
            except Exception:
                pass
                
        _ai_service_instance = AIService(provider=provider)
    return _ai_service_instance


_ai_service_instance: AIService | None = None
