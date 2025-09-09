import re

def search_sop_content(sop_texts, query):
    # Normalize the query to lowercase for case-insensitive matching
    query = query.lower()

    # Split the query into individual words (tokens)
    query_tokens = query.split()

    # Iterate over the SOP texts and search for the query
    for text in sop_texts:
        # Clean the SOP text by removing extra spaces and normalizing case
        cleaned_text = text.lower()

        # Check if any of the query tokens appear in the SOP text
        if any(token in cleaned_text for token in query_tokens):
            return text  # Return the full text or a snippet

    return None

