# Prompt Processing
The `prompt-processing` folder contains the necessary files and scripts for processing user prompts before sending to the LLM.

## Updates needed

- Need to split the amount of text and parallelize for spell checking and grammar processing. Currently, it only uses a single thread, which takes quite a while to process more than 10,000 words.
