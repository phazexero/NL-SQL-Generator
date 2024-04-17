import os
from together import Together
import argparse

def generate_prompt(question, prompt_file="prompt.md", metadata_file="metadata.sql"):
    with open(prompt_file, "r") as f:
        prompt = f.read()
    
    with open(metadata_file, "r") as f:
        table_metadata_string = f.read()

    prompt = prompt.format(
        user_question=question, table_metadata_string=table_metadata_string
    )
    return prompt

def generate_sql(question):
    client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
    response = client.completions.create(
        model="mistralai/Mistral-7B-v0.1",
        prompt=generate_prompt(question, prompt_file="prompt.md", metadata_file="metadata.sql"),
        # max_tokens = 100
        stop = ["[/SQL]"]
    )
    # print(response)
    return response.choices[0].text

if __name__ == "__main__":
    # Parse arguments
    _default_question="Identify ledgers created in the last month that have attachments with a specific file extension (e.g., '.pdf')"

    parser = argparse.ArgumentParser(description="Run inference on a question")
    parser.add_argument("-q","--question", type=str, default=_default_question, help="Question to run inference on")
    args = parser.parse_args()
    question = args.question
    print("Loading a model and generating a postgres query for answering your question...")
    print(generate_sql(question))