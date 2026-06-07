from pathlib import Path
import tempfile

import streamlit as st
from PIL import Image

from app.document_processor import ingest_file
from app.rag import ask_compliance_copilot


st.set_page_config(
    page_title="Enterprise Document Intelligence",
    page_icon="🛡️",
    layout="wide"
)


@st.cache_resource
def load_logo():
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        return Image.open(logo_path)
    return None


logo = load_logo()

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 750;
        margin-bottom: 0.15rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        padding: 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        background-color: #f9fafb;
    }
    .footer-note {
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


header_col1, header_col2 = st.columns([1, 6])

with header_col1:
    if logo:
        st.image(logo, width=110)
    else:
        st.markdown("## 🛡️")

with header_col2:
    st.markdown(
        '<div class="main-title">Enterprise Document Intelligence</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">AI-powered document analysis, semantic search, and source-grounded question answering.</div>',
        unsafe_allow_html=True
    )


with st.sidebar:
    if logo:
        st.image(logo, width=90)

    st.header("Platform Overview")
    st.info(
        "Upload enterprise documents, generate an AI summary, and ask "
        "natural-language questions with source-grounded answers."
    )

    st.markdown("---")

    st.subheader("Supported Formats")
    st.write("• PDF")
    st.write("• TXT")
    st.write("• Markdown")

    st.markdown("---")

    st.subheader("Technology Stack")
    st.write("• Azure OpenAI")
    st.write("• LangChain")
    st.write("• ChromaDB")
    st.write("• FastAPI")
    st.write("• Streamlit")

    st.markdown("---")
    st.caption("Built for enterprise document intelligence, compliance, policy search, and knowledge discovery.")


st.markdown("---")

top_col1, top_col2, top_col3 = st.columns(3)

with top_col1:
    st.markdown('<div class="metric-card"><b>Document Upload</b><br/>PDF, TXT, Markdown</div>', unsafe_allow_html=True)

with top_col2:
    st.markdown('<div class="metric-card"><b>AI Analysis</b><br/>Summary, topics, questions</div>', unsafe_allow_html=True)

with top_col3:
    st.markdown('<div class="metric-card"><b>Grounded Answers</b><br/>RAG with source excerpts</div>', unsafe_allow_html=True)


st.markdown("")

left_col, right_col = st.columns([1, 1], gap="large")


with left_col:
    st.subheader("📄 Document Upload")

    uploaded_file = st.file_uploader(
        "Upload a policy, manual, brochure, contract, or other enterprise document.",
        type=["pdf", "txt", "md"]
    )

    if uploaded_file:
        st.caption(f"Selected file: {uploaded_file.name}")

    if uploaded_file and st.button("Upload and Analyze Document", use_container_width=True):
        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = Path(tmp.name)

        with st.spinner("Indexing and analyzing document..."):
            result = ingest_file(tmp_path)

        st.success(
            f"Uploaded and indexed: {uploaded_file.name} | "
            f"Chunks created: {result['chunks_created']}"
        )

        st.subheader("Document Analysis")
        st.markdown(result["analysis"])


with right_col:
    st.subheader("🔍 Document Search")

    question = st.text_area(
        "Ask a question about the uploaded documents.",
        placeholder="Example: Can employees store customer SIN numbers in any system?",
        height=150
    )

    example_questions = [
        "Summarize the key requirements in this document.",
        "What are the main obligations or rules?",
        "What are the important dates, timelines, or deadlines?",
        "What are the risks or restrictions mentioned?",
    ]

    selected_example = st.selectbox(
        "Or try an example question",
        [""] + example_questions
    )

    if selected_example and not question:
        question = selected_example

    if st.button("Search Documents", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching documents and generating answer..."):
                result = ask_compliance_copilot(question)

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")
            for source in result["sources"]:
                with st.expander(source["document"]):
                    st.write(source["excerpt"])


st.markdown(
    '<div class="footer-note">Enterprise Document Intelligence demo using Azure OpenAI, semantic retrieval, and source-grounded responses.</div>',
    unsafe_allow_html=True
)