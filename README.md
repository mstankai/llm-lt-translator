# LLM based Lithuanian language translator

A document translator from English to Lithuanian (or other languages).
Based on OpenAI's API.

## Table of Contents

- [About](#about)
- [Setup](#setup)
- [Usage](#usage)
- [Cool Insights](#cool-insights)
- [Future To Do's and Ideas](#future-to-dos-and-ideas)
- [License](#license)

## About
The translator reads DOCX files, translates the content while _atempting_ to preserve formatting,
and outputs the translated text in a new DOCX file.

The formatting preservation is not working great the moment,
but I may be limited in what I can _easily_ do, by the capabilities of the `python-docx` library.

The user can select the output language, but in the future,
the app will be optimised for translations between English and Lithuanian.

This code is primarily written to support my family with translations,
so I will be prioritising functionalities that would be useful to them.


## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/mstankai/llm-lt-translator.git
    cd llm-lt-translator
    ```

1. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

1. **Install dependencies :**
    ```sh
    pip install -r requirements.txt
    ```

1. **Set up OpenAI API key:**
    You can set up an API key on the Open AI Platform page, here: [OpenAI Platform | API Keys](https://platform.openai.com/api-keys).

    Store your OpenAI API key in your system's keychain using the following command:
    ```sh
    python -c 'import keyring; keyring.set_password("system", "openai_api_key", "<your-api-key>")'
    ```sh


## Usage

To translate a DOCX file, run the following command:

```sh
python doc_translator.py <input-file> [-o <output-file>] [-m <model>] [-l <language>] [-v] [--dry-run]
```


## Cool insights
- Given that the tokenizer embedings were likely not trained on the lithuanian language, lithuanian text, on averge, has more tokens than in english.

## Future TO DO's and Ideas

### High Priority
- [ ] Expand to PDFs
- [ ] Save metadata to database
- [ ] The translation isn't great, perhaps I can scrape an [english - lithuanian] dictionary and add a RAG

### Fun Stuff
- [ ] Run a study of token differences for different languages. Estimate output token quantity and cost.
- [ ] Detect input language
- [ ] The current tokenizer encodings aren't made for Lithuanian. Explore if I could improve translation through encoding training.

### Low Priority
- [ ] The docx formatting is not really working

## License

Distributed under the GNU GENERAL PUBLIC LICENSE v3.0. See `LICENSE` for more information.
