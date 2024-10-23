from openai import OpenAI
from docx import Document
import tiktoken
import yaml
import keyring
import argparse
import sys

def system_prompt(language):
    return f"""
    You are a skilled {language} language translator. Your goal is to provide translations that are:
    Accurate: Convey the exact meaning of the original text, including idioms and cultural references.
    Fluent: Ensure the translation reads naturally and smoothly in the target language.
    Culturally Appropriate: Adapt the text for the target audience while respecting cultural differences.
    Consistent: Maintain tone, style, and terminology throughout the translation.
    Context-Aware: Understand and accurately translate technical or specialized terms relevant to the text's field.
    """


def get_api_key(key_name):
    api_key = keyring.get_password("system", key_name)
    if api_key is None:
        raise ValueError("API key not found in Keychain!")
    return api_key


def read_docx(file_path):
    
    doc = Document(file_path)

    texts = []
    formats = []

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:

            run_format = {
                'bold': run.bold,
                'italic': run.italic,
                'underline': run.underline,
                'font_name': run.font.name,
                'font_size': run.font.size.pt if run.font.size else None,
                'font_color': run.font.color.rgb if run.font.color else None,
            }

            texts.append(run.text)
            formats.append(run_format)

    return texts, formats

def get_number_of_tokens(messages, model_name):

    # get tokenizer encoding
    encoding = tiktoken.encoding_for_model(model_name)

    # counting tokens from each message
    token_count = 0
    for m in messages:
        text = m['content']
        tokens  = encoding.encode(text)
        token_count += len(tokens)

    return token_count

def get_cost_of_tokens(n_tokens, model_name, is_input=True):

    # get price list
    with open(TOKEN_PRICE_LIST_PATH, 'r') as f:
        price_list = yaml.safe_load(f)
    
    # get pice list keys for model
    model_group = MODEL_TYPE + "_models"
    token_type = "input_tokens" if is_input else "output_tokens"

    cost_per_1M_tokens = price_list[model_group][model_name][token_type]
    cost = cost_per_1M_tokens * n_tokens / 1e6

    return cost    

def get_completion(messages, model_name):
    
    completion_input = dict(
        model=model_name,
        messages=messages
    )
        
    completion = client.chat.completions.create(**completion_input)
    return completion.choices[0]


# ------------------------------------------
if __name__ == "__main__":

    # constants
    TOKEN_PRICE_LIST_PATH = "etc/openai_pricing_23Oct2024.yaml"
    MODEL_TYPE = "chat"

    # get arguments
    parser = argparse.ArgumentParser(description='Translate a PDF file to a selected language')
    parser.add_argument('input')
    parser.add_argument('-o','--output', default='output/output.txt')
    parser.add_argument('-l','--lang', default='Lithuanian')
    parser.add_argument('-v','--verbose', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
        
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    language = args.lang
    verbose = args.verbose
    dry_run = args.dry_run

    # get text
    text_list, formatting_list = read_docx(input_file)
    
    # set up OpenAI API
    openai_api_key = get_api_key("openai_api_key")
    client = OpenAI(api_key=openai_api_key)
    model_name = "gpt-4o-mini"

    # transform text to OpenAI messages format
    messages = [{'role': 'system', 'content': system_prompt(language)}]
    for t in text_list:
        messages += [{'role': 'user', 'content': t}]

    # get number of tokens
    n_input_tokens = get_number_of_tokens(messages, model_name)
    input_cost = get_cost_of_tokens(n_input_tokens, model_name, is_input=True)

    print(f"Input file: {input_file}")
    print()
    print(f"Submitting {len(messages)} messages to OpenAI API...")
    print(f"Number of tokens: {n_input_tokens}")
    print(f"Estimated cost of input: {input_cost} USD")


    if verbose:
        print("Messages:")
        for m in messages:
            print(f"{m['role']}: {m['content']}")
        print()


    if dry_run:
        print("Dry run. Not submittion is made.")
    else:
        completion=get_completion(messages, model_name)
        if verbose:
            print(completion)
        
        print()
        print(completion.message.content)
        
    print("Translation completed.")



    # print(completion.choices[0])