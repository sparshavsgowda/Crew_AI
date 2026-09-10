"""Streamlit view for the banking assistant."""

from __future__ import annotations

import streamlit as st
from tenacity import RetryError

from controllers.banking_controller import BankingController
from models.database import create_database


def render() -> None:
    st.set_page_config(page_title="Crew Banking Assistant", page_icon="🏦", layout="centered")
    create_database()
    controller = BankingController()

    st.title("Crew Banking Assistant")
    st.caption("Demo mode · fixed user: USER-1001 · account: ACCT-1001")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome. Ask about balances, transactions, spending, or a service request."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a banking question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Checking the banking specialists..."):
                try:
                    answer = controller.answer(prompt)
                except RetryError:
                    answer = "The banking service is temporarily rate-limited after several retries. Please try again in a moment."
                except Exception as error:
                    error_text = str(error).lower()
                    if "429" in error_text or "rate limit" in error_text or "too many requests" in error_text:
                        answer = "The banking service is rate-limited right now. Please try again shortly."
                    else:
                        answer = "I could not complete that request. Please try again."
                        st.session_state.last_error = str(error)
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.sidebar:
        st.subheader("Demo context")
        st.write("No authentication is enabled.")
        st.write("Data is recreated on startup.")
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()
