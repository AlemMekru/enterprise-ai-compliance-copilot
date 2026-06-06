from app.azure_client import get_chat_model


def analyze_document(text: str):

    llm = get_chat_model()

    prompt = f"""
You are an enterprise document analyst.

Analyze the document and return:

1. Document Type
2. Short Summary
3. Key Topics (5 maximum)
4. Suggested Questions (5 maximum)

Document:

{text[:12000]}
"""

    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":

    sample_text = """
    This document describes a Doctor of Technology in Artificial Intelligence
    program including admissions, tuition, curriculum and graduation requirements.
    """

    result = analyze_document(sample_text)

    print(result)