import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from utils.docx_parser import parse_docx
from utils.pdf_parser import parse_pdf
from utils.image_parser import parse_image
import os

# Load pre-trained GPT-2 model and tokenizer from Hugging Face
model_name = "gpt2"  # You can use "gpt2-medium" or "gpt2-large" for larger models
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set pad_token_id to eos_token_id, since GPT-2 doesn't have a dedicated pad token
tokenizer.pad_token = tokenizer.eos_token  # Set padding token to eos_token
model.config.pad_token_id = tokenizer.eos_token_id  # Ensure the model uses eos_token as pad token

SOP_DIRECTORY = "documents/"
MAX_TOKENS = 1024  # Set a limit to keep token count under the model's max limit (e.g., 1024)

def extract_relevant_section(text, section_keywords):
    """Extracts the relevant section from SOP text based on section name"""
    print(f"Extracting sections with keywords: {section_keywords}")

    # Build the regex pattern to match any of the section keywords (case-insensitive)
    keywords_pattern = '|'.join([re.escape(keyword) for keyword in section_keywords])
    pattern = re.compile(rf"({keywords_pattern}.*?)(?=\n|Introduction|Post-Test|Steps|Operational|Counselling)", re.IGNORECASE | re.DOTALL)

    # Debug: Print the SOP content to verify if it's correct
    print(f"SOP content snippet: {text[:500]}")

    # Search for section using the updated pattern
    matches = re.findall(pattern, text)

    if matches:
        section_text = matches[0][0]  # Get the text of the matched section
        return section_text.strip()
    else:
        print("No relevant section found!")
        return None

def split_into_chunks(text, max_tokens=MAX_TOKENS):
    """Splits SOP text into chunks based on the token limit"""
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk) for chunk in chunks]

def query_sop(user_query, consent=False):
    sop_files = os.listdir(SOP_DIRECTORY)
    sop_texts = []

    # Iterate over SOP files and extract their content
    for sop_file in sop_files:
        file_path = os.path.join(SOP_DIRECTORY, sop_file)
        if sop_file.startswith("~$"):
            continue
        if sop_file.endswith(".pdf"):
            sop_texts.append(parse_pdf(file_path))
        elif sop_file.endswith(".docx"):
            sop_texts.append(parse_docx(file_path))
        elif sop_file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            sop_texts.append(parse_image(file_path))  # Extract text from image

    # Combine all SOP text into one large string
    sop_content = " ".join(sop_texts)

    # If no SOP content is found, return a fallback message
    if not sop_content.strip():
        return "No SOP content found. Would you like me to search the web for you?"

    # Debug: Print first 1000 characters of SOP content for inspection
    print(f"First 1000 characters of SOP content: {sop_content[:1000]}")

    # Define the section keywords we're interested in
    section_keywords = ["Steps for HIV negative Post-Test Counselling", "HIV negative Post-Test Counselling", "Post-Test Counselling"]

    # Extract relevant section from the SOP based on the query
    relevant_section = extract_relevant_section(sop_content, section_keywords)
    if relevant_section is None:
        return "No relevant section found in SOPs."

    # Debug: Print the extracted relevant section to inspect
    print(f"Extracted relevant section: {relevant_section[:500]}...")

    # Split relevant section into smaller chunks to fit within the model's token limit
    chunks = split_into_chunks(relevant_section)

    # Generate a response for each chunk
    answers = []
    for chunk in chunks:
        prompt = f"Answer the following question based on the SOP content: {user_query}\n\nSOP Content:\n{chunk}"

        # Encode the prompt text and generate a response using GPT-2
        inputs = tokenizer.encode(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)

        # Create attention mask to indicate where padding occurs
        attention_mask = inputs.new_ones(inputs.shape)  # Create a mask with 1s for actual tokens and 0s for padding

        # Generate a response, ensuring that the output doesn't exceed the token limit
        outputs = model.generate(
            inputs, 
            max_new_tokens=150,  # Set maximum number of tokens to generate for output
            num_return_sequences=1, 
            no_repeat_ngram_size=2, 
            temperature=0.7,
            attention_mask=attention_mask,  # Pass the attention mask
            pad_token_id=tokenizer.eos_token_id  # Ensure proper padding
        )

        # Decode and add the answer
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()
        if answer:
            answers.append(answer)

    # If no answer found in the chunks, proceed with web search or fallback
    if answers:
        return " ".join(answers)
    elif consent:
        web_result = search_web(user_query)
        return web_result
    else:
        return "No answer found in SOPs. Would you like me to search the web for you?"
