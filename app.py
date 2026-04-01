import os
import pandas as pd
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

#API key and model 
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-2024-11-20")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")
client = OpenAI(api_key=API_KEY)

def segment_text(text, few_shot_prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a linguistic annotator."},
                {
                    "role": "user",
                    "content": few_shot_prompt.strip() + "\n\nInput:\n" + text.strip(),
                },
            ],
            temperature=0,
            top_p = 1, 
            seed = 42
        )
        output = response.choices[0].message.content.strip()
        lines = [line.strip() for line in output.split("\n") if line.strip()]
        return lines
    except Exception as e:
        return [f"Error: {e}"]

def run_segmentation(file, prompt):
    if file is None or prompt is None:
        return "Please upload a tab-delimited file with id and text columns."

    df = pd.read_csv(file.name, sep="\t")

    with open(prompt.name, "r", encoding="utf-8") as f:
            few_shot_prompt = f.read()

    if not {"id", "text"}.issubset(df.columns):
        return "File must contain columns: id and text."

    parsed_rows = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        pid = str(row["id"])
        text = str(row["text"])
        ideas = segment_text(text, few_shot_prompt)
        for idea in ideas:
            parsed_rows.append({"id": pid, "text": idea})

    out_df = pd.DataFrame(parsed_rows)
    out_path = "parsed_output.txt"
    out_df.to_csv(out_path, sep="\t", index=False)
    return out_path

#Gradio Interface
with gr.Blocks(title="LLM Idea Parser") as demo:
    gr.Markdown(
        "## LLM Idea Parsing Tool\n"
        "Upload a tab-delimited input file with `id` and `text` columns, and a .txt file containing the prompt."
    )
    file_input = gr.File(label="Upload Input File (tab-delimited .txt)")
    prompt_input = gr.File(label="Upload Prompt File (.txt)")

    run_button = gr.Button("Run")
    output_file = gr.File(label="Download Parsed Output (.txt)")

    run_button.click(
        fn=run_segmentation,
        inputs=[file_input, prompt_input],
        outputs=output_file,
    )

demo.launch()
