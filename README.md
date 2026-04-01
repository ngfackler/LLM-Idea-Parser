# LLM Idea Parser

Segments text into discrete ideas using an LLM (OpenAI GPT-4o) via a Gradio interface.

Author: Nikki Fackler Kaye

## Overview

This application:
- Takes a tab-delimited file containing text data
- Uses a few-shot prompt to guide idea parsing
- Sends each text to an LLM
- Returns a structured output with one idea per row

## Input Format

The input file must be a tab-delimited `.txt` file with the following columns:

| id | text |
|----|------|
| 1  | Example text here |
| 2  | Another example |

## Prompt Format

Upload a `.txt` file containing your few-shot prompt.

The prompt should:
- Define what constitutes an "idea"  
  (e.g., *"Your task is to segment the following text into discrete propositions that express predications of a verb (a statement that attributes an action, state, or relation to a subject). A single sentence can contain multiple propositions of this sort. Separate these propositions using the rules and examples below."*)
- Include examples (recommended)

  **Examples:**
  Input:
  The primary colors are red, blue, and yellow.
  Output:
  The primary colors are red.
  The primary colors are blue.
  The primary colors are yellow.
  
  Input:
  Earth, which orbits the Sun, is the third planet.
  Output:
  Earth is the third planet.
  Earth orbits the Sun.

## Output

The tool generates a tab-delimited `.txt` file called `parsed_output.txt` in the project directory with:

| id | text |
|----|------|
| 1  | First idea |
| 1  | Second idea |
| 1  | Third idea |
| 2  | First idea |
| 2  | Second idea |
etc.

Each row corresponds to one segmented idea.

## API Notes

- Create a `.env` file in the project directory with the following text:
OPENAI_API_KEY=your_api_key_here
- The default model used is `gpt-4o-2024-11-20` - can change this in app.py
- If there is an API error, the output will include a row with an error message (e.g., `API_ERROR: ...`) 
- Output quality depends heavily on prompt design

