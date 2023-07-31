import json
import guidance
######################## THIS IS STILL A WIP ########################
# Goal: Applying https://github.com/microsoft/guidance to a Llmma-2
# model fine-tuned as a coding assistant. By restricting its output
# format we can easily guide it to providing a consistent response.
# Need to figure out how to load these models locally-- as opposed to
# fetching from HF
#####################################################################

llm = guidance.llms.Transformers("path/to/model")

# Define the guidance program
code_generator = guidance('''
{{#system~}}
You are a helpful assistant, that communicates ONLY and strictly ONLY with python code.
The code must include any necessary function definitions and must also include commands 
to run these functions and print the results.

The goal is to have a complete, runnable Python script in each response.

Your responses MUST absolutely follow the format below:

python
{CODE}
NOTE: If you are not able to provide an answer despite all your efforts you may simply 
reply with that reason.

OBS: DO NOT INCLUDE ANY EXPLANATION. ONLY CODE.
{{~/system}}

{{#user~}}
{{prompt}}
{{~/user}}

{{#assistant to=python code~}}
{{gen 'python_code' temperature=0 max_tokens=500}}
{{~/assistant}}
''', llm=llama)

# To use the program, provide the prompt as a string:
output = code_generator(prompt='Write a python function to calculate factorial of a number.')

print(output)
