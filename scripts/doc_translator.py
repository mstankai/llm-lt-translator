from openai import OpenAI
import keyring
import argparse


def get_api_key(key_name):
    api_key = keyring.get_password("system", key_name)
    if api_key is None:
        raise ValueError("API key not found in Keychain!")
    return api_key



# ------------------------------------------
if __name__ == "__main__":

    # get arguments
    parser = argparse.ArgumentParser(description='Translate a PDF file to Lithuanian.')
    parser.add_argument('input')
    parser.add_argument('-o','--output', default='output/output.txt')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    # get OpenAI API Key
    openai_api_key = get_api_key("openai_api_key")
    client = OpenAI(api_key=openai_api_key)


    # Hello World API Test
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about naughty black kittens."
            }
        ]
    )

    print(completion.choices[0].message)