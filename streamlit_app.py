from pathlib import Path
from urllib import error, request
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Farmer Market Connect", layout="wide")

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "").strip()
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


def call_gemini(prompt: str, system_instruction: str = "", model: str = "gemini-2.5-flash") -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in Streamlit Secrets.")

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1200, "temperature": 0.5},
    }
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    url = f"{GEMINI_BASE}/{model}:generateContent"
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini HTTP {exc.code}: {body[:200]}") from exc
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed: {exc}") from exc

    parts = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [])
    )
    text = "".join(part.get("text", "") for part in parts).strip()
    if not text:
        raise RuntimeError("Empty response returned by Gemini.")
    return text


html_path = Path(__file__).parent / "index.html"
html_content = html_path.read_text(encoding="utf-8")

components.html(html_content, height=900, scrolling=True)

with st.expander("Server-Side Krishi AI (Uses st.secrets Safely)"):
    if not GEMINI_API_KEY:
        st.warning(
            "Add `GEMINI_API_KEY = \"...\"` in Streamlit Cloud **Settings → Secrets** "
            "(or in `.streamlit/secrets.toml` locally) to enable server-side AI calls."
        )
    else:
        selected_model = st.selectbox("Model", DEFAULT_MODELS, index=0)
        user_prompt = st.text_area("Ask Krishi AI", placeholder="How can I improve soil fertility or sell my crop?")
        if st.button("Ask AI"):
            if not user_prompt.strip():
                st.error("Please enter a question first.")
            else:
                with st.spinner("Contacting Gemini..."):
                    try:
                        reply = call_gemini(
                            prompt=user_prompt.strip(),
                            system_instruction=(
                                "You are Krishi AI, a practical agricultural assistant for farmers in India. "
                                "Keep explanations clear, cautious, and easy to follow."
                            ),
                            model=selected_model,
                        )
                        st.markdown(reply)
                    except Exception as err:
                        st.error(str(err))
