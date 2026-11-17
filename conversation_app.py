
import streamlit as st

from rag.query_rewriter import rewrite_followup_question
from rag.answer_generator import (
    generate_answer,
    build_evidence_context
)
from retrieval.hybrid_search import hybrid_search
from rag.evidence_validator import validate_answer
from rag.language_support import (
    get_language_from_choice,
    detect_language_from_text,
)
from rag.multilingual import translate_query_for_retrieval

from farmer_profile import render_farmer_profile
from profile_storage import save_profile
from eligibility_engine import assess_scheme


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Farming Chitti",
    page_icon="🌾",
    layout="wide"
)


# --------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "farmer_profile" not in st.session_state:
    st.session_state.farmer_profile = None

if "saved_profile_snapshot" not in st.session_state:
    st.session_state.saved_profile_snapshot = None


# --------------------------------------------------
# 3. APPLICATION HEADER
# --------------------------------------------------

st.title("🌾 Farming Chitti")
st.caption("AI-Powered Multilingual Farmer Assistant")

st.divider()


# --------------------------------------------------
# 4. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🌾 Farming Chitti")

menu = st.sidebar.radio(
    "Select Module",
    [
        "AI Farmer Assistant",
        "Farmer Profile",
        "Scheme Eligibility"
    ]
)


# --------------------------------------------------
# 5. AI FARMER ASSISTANT
# --------------------------------------------------

if menu == "AI Farmer Assistant":

    st.header("💬 AI Farmer Assistant")

    language_options = {
        "Auto Detect": "0",
        "English": "1",
        "Tamil": "2",
        "Hindi": "3",
        "Telugu": "4",
        "Kannada": "5",
        "Malayalam": "6"
    }

    selected_language = st.selectbox(
        "Select Response Language",
        list(language_options.keys())
    )

    language_choice = language_options[selected_language]

    # Display previous conversation
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("Document Sources"):
                    for source in message["sources"]:
                        st.write(source)

    # Chat input
    question = st.chat_input(
        "Ask your farming question..."
    )

    if question:

        # Display farmer question
        with st.chat_message("user"):
            st.markdown(question)

        previous_questions = [
            message["content"]
            for message in st.session_state.chat_history
            if message["role"] == "user"
        ]

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        try:

            with st.chat_message("assistant"):

                with st.spinner("Farming Chitti is processing your question..."):

                    # Language detection
                    response_language = (
                        detect_language_from_text(question)
                        if language_choice == "0"
                        else get_language_from_choice(language_choice)
                    )

                    # Rewrite follow-up question
                    rewritten_question = rewrite_followup_question(
                        current_question=question,
                        conversation_history=previous_questions
                    )

                    # Translate query for retrieval
                    retrieval_query = translate_query_for_retrieval(
                        rewritten_question,
                        response_language
                    )

                    # Retrieve relevant documents
                    retrieved_results = hybrid_search(
                        retrieval_query,
                        candidate_k=10,
                        final_k=5
                    )

                    # Generate answer
                    result = generate_answer(
                        question=question,
                        retrieved_results=retrieved_results,
                        response_language=response_language
                    )

                    # Evidence validation
                    evidence_context, sources = build_evidence_context(
                        retrieved_results
                    )

                    validation = validate_answer(
                        answer=result["answer"],
                        evidence_context=evidence_context
                    )

                    if validation["is_valid"]:

                        answer = result["answer"]

                        st.markdown(answer)

                        if sources:
                            with st.expander("Document Sources"):
                                for source in sources:
                                    st.write(source)

                    else:

                        answer = (
                            "I could not verify this answer against "
                            "the uploaded government documents. "
                            "Please consult the official scheme guidelines."
                        )

                        st.warning(answer)

                        st.write(
                            "Validation reason:",
                            validation.get("reason", "Not available")
                        )

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources if validation["is_valid"] else []
                    })

        except Exception as error:

            st.error("An error occurred while processing your question.")

            st.exception(error)

    # Clear conversation
    if st.sidebar.button("Clear Conversation"):

        st.session_state.chat_history = []
        st.rerun()


# --------------------------------------------------
# 6. FARMER PROFILE
# --------------------------------------------------

elif menu == "Farmer Profile":

    st.header("👨‍🌾 Farmer Registration")

    profile = render_farmer_profile()

    if profile:

        st.session_state.farmer_profile = profile

        # Avoid duplicate profile storage on reruns
        if (
            st.session_state.saved_profile_snapshot
            != profile
        ):

            save_profile(profile)

            st.session_state.saved_profile_snapshot = profile

            st.success("Farmer profile saved successfully!")

    elif st.session_state.farmer_profile:

        st.subheader("Current Farmer Profile")

        st.json(st.session_state.farmer_profile)


# --------------------------------------------------
# 7. SCHEME ELIGIBILITY
# --------------------------------------------------

elif menu == "Scheme Eligibility":

    st.header("📋 Preliminary Scheme Eligibility")

    profile = st.session_state.get("farmer_profile")

    if not profile:

        st.warning(
            "Please register your farmer profile "
            "before checking scheme eligibility."
        )

        st.info(
            "Go to Farmer Profile and complete registration."
        )

    else:

        st.subheader("Farmer Information")

        st.write("Farmer:", profile.get("name"))
        st.write("State:", profile.get("state"))
        st.write("District:", profile.get("district"))
        st.write("Crop:", profile.get("crop"))
        st.write("Land Ownership:", profile.get("land_ownership"))

        st.divider()

        st.subheader("Scheme Assessment")

        schemes = [
            "PM-KISAN",
            "PM Fasal Bima Yojana",
            "Kisan Credit Card"
        ]

        for scheme in schemes:

            with st.expander(scheme, expanded=True):

                result = assess_scheme(profile, scheme)

                st.info(result["status"])

                st.write("Assessment details:")

                for reason in result["reasons"]:
                    st.write("-", reason)

                st.caption(
                    "This is a preliminary assessment, "
                    "not official approval or confirmation of eligibility."
                )


# --------------------------------------------------
# 8. APPLICATION FOOTER
# --------------------------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "Farming Chitti | AI Agriculture Assistant"
)
