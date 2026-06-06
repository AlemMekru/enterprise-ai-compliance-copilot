from pathlib import Path
import tempfile

import streamlit as st

from app.document_processor import ingest_file
from app.rag import ask_compliance_copilot


st.set_page_config(
    page_title="Enterprise AI Compliance Copilot",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Enterprise Document Intelligence")

st.caption("AI-powered document analysis, semantic search, and question answering with source citations.")

st.header("1. Upload Policy / Compliance Document")

uploaded_file = st.file_uploader(
    "Supported formats: PDF, TXT, Markdown",
    type=["pdf", "txt", "md"]
)

if uploaded_file and st.button("Upload and Index Document"):
    suffix = Path(uploaded_file.name).suffix

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = Path(tmp.name)

    result = ingest_file(tmp_path)

    st.success(
        f"Uploaded and indexed {uploaded_file.name}. "
        f"Chunks created: {result['chunks_created']}"
    )

    st.subheader("Document Analysis")
    st.markdown(result["analysis"])

st.header("2. Ask a Compliance Question")

question = st.text_area(
    "Question",
    placeholder="Can employees store customer SIN numbers in any system?"
)

if st.button("Search Documents"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing documents..."):
            result = ask_compliance_copilot(question)
        
        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")
        for source in result["sources"]:
            with st.expander(source["document"]):
                st.write(source["excerpt"])