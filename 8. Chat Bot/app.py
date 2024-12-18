from utils.get_index import * 
from utils.prompt_func import *

from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.core import Settings

import os
os.environ['CURL_CA_BUNDLE'] = ''

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from dotenv import load_dotenv
load_dotenv()

token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

Settings.llm = HuggingFaceInferenceAPI(
    # model_name="HuggingFaceH4/zephyr-7b-beta",
    model_name="mistralai/Mistral-7B-Instruct-v0.3",
    token=token,
    context_window=3900,
    max_new_tokens=256,
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    device_map="auto",
)

print("Setting up the QA bot...🤖")
index = create_index()


def final_result(query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response, query


def format_output(answer, query):
    result = f"**Question:** {query} 🤔\n\n"
    result += f"**Answer:** 💡 {answer.response} 🙏\n\n"

    if answer.source_nodes:
        result += "You can read more of it at: \n"
        for node in answer.source_nodes:
            # Extracting metadata
            metadata = node.node.metadata
            page = metadata.get('page_label', 'N/A')
            source = metadata.get('file_name', 'N/A')

            # Formatting the source information
            result += f"- Page {page} from {source}\n"
        result += "\n"

    result += "What would you like to know more?"

    return result

def main():

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response, query = final_result(user_input)
        formatted_output = format_output(response, query)
        print("Bot:", formatted_output)

if __name__ == '__main__':
    main()