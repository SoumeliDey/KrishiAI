import json
from pathlib import Path
from urllib import error, request

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Farmer Market Connect", layout="wide")


def get_gemini_api_key() -> str:
    """Safely read GEMINI_API_KEY from st.secrets without crashing if secrets are unset."""
    try:
        raw_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""
    return raw_key.strip() if isinstance(raw_key, str) else ""


GEMINI_API_KEY = get_gemini_api_key()
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
]


def call_gemini_once(
    prompt: str,
    model: str,
    system_instruction: str = "",
) -> str:
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 1200,
            "temperature": 0.5,
        },
    }
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

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

    candidates = data.get("candidates") or []
    first = candidates[0] if candidates else {}
    parts = (first.get("content") or {}).get("parts") or []
    text = "".join(part.get("text", "") for part in parts if isinstance(part, dict)).strip()
    if not text:
        raise RuntimeError("Empty response returned by Gemini.")
    return text


def call_gemini(
    prompt: str,
    system_instruction: str = "",
    preferred_model: str = "gemini-3.8-flash",
) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in Streamlit Secrets.")

    candidates_to_try = []
    for m in [preferred_model, *DEFAULT_MODELS]:
        if m and m not in candidates_to_try:
            candidates_to_try.append(m)

    last_error = None
    for model_name in candidates_to_try:
        try:
            return call_gemini_once(
                prompt=prompt,
                model=model_name,
                system_instruction=system_instruction,
            )
        except Exception as err:
            last_error = err
            msg = str(err)
            # Only fall back to another model if the model endpoint itself is unavailable/not found
            if "HTTP 404" in msg or "not found" in msg.lower():
                continue
            raise

    raise last_error if last_error else RuntimeError("No available Gemini model succeeded.")


def render_frontend() -> None:
    html_path = Path(__file__).parent / "index.html"
    if not html_path.exists():
        st.error("index.html was not found next to streamlit_app.py.")
        return

    html_content = html_path.read_text(encoding="utf-8")
    components.html(html_content, height=900, scrolling=True)


@st.fragment
def krishi_ai_section() -> None:
    with st.expander("Server-Side Krishi AI (Uses st.secrets Safely)", expanded=True):
        if not GEMINI_API_KEY:
            st.warning(
                'Add `GEMINI_API_KEY = "your-key"` in Streamlit Cloud **Settings -> Secrets** '
                "(or in `.streamlit/secrets.toml` locally, which must be ignored by Git) "
                "to enable server-side AI calls."
            )
            return

        selected_model = st.selectbox("Model", DEFAULT_MODELS, index=0, key="krishi_model")
        user_prompt = st.text_area(
            "Ask Krishi AI",
            placeholder="How can I improve soil fertility or sell my crop?",
            key="krishi_prompt",
        )
        if st.button("Ask AI", key="krishi_ask_btn"):
            if not user_prompt.strip():
                st.error("Please enter a question first.")
            else:
                with st.spinner("Contacting Gemini..."):
                    try:
                        reply = call_gemini(
                            prompt=user_prompt.strip(),
                            system_instruction=(
                                "You are Krishi AI, a practical agricultural assistant for farmers in India. "
                                "Keep explanations simple, cautious, and easy to follow. Do not invent schemes, "
                                "prices, or chemical instructions, and advise consulting local experts when unsure."
                            ),
                            preferred_model=selected_model,
                        )
                        st.markdown(reply)
                    except Exception as err:
                        st.error(str(err))


render_frontend()
krishi_ai_section()
