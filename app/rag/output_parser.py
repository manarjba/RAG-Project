# app/rag/output_parser.py

def parse_response(raw_response: str) -> str:
    """
    Cleans and formats the raw response from the LLM.

    Args:
        raw_response (str): The raw text returned by the LLM.

    Returns:
        str: A cleaned and user-friendly version of the response.
    """
    if not raw_response:
        return "⚠️ No response received from the language model."

    # Strip unnecessary whitespace and ensure clean formatting
    cleaned = raw_response.strip()

    # Optionally, you could add more formatting logic here
    return cleaned
# app/rag/output_parser.py

def parse_llm_output(output: str) -> str:
    """
    Parses and cleans the output from the LLM before returning to the user.
    For now, just strip whitespace.
    """
    return output.strip()
