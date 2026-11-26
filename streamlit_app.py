@st.fragment
def krishi_ai_section():
    with st.expander("Server-Side Krishi AI (Uses st.secrets Safely)", expanded=True):
        if not GEMINI_API_KEY:
            st.warning(
                'Add `GEMINI_API_KEY = "..."` in Streamlit Cloud **Settings → Secrets** '
                "(or in `.streamlit/secrets.toml` locally) to enable server-side AI calls."
            )
            return

        selected_model = st.selectbox("Model", DEFAULT_MODELS, index=0)
        user_prompt = st.text_area(
            "Ask Krishi AI",
            placeholder="How can I improve soil fertility or sell my crop?",
        )
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


krishi_ai_section()
