from flask import Flask, request
import re
import subprocess
from flask_cors import CORS
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Flask App
app = Flask(__name__)
CORS(app)

# for some reason I'm getting extremely slow inference speeds with WizardLM-13B-V1.2
WIZARD_LM_V2 = "WizardLM-13B-V1.2/WizardLM-13B-V1.2-GGML-q4_0.bin"
USEFUL_CODER = "code_cherry_Llama_q4_0.bin"

MODEL = f"models/{USEFUL_CODER}"

def run_python_code(code):
    process = subprocess.Popen(["python3", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()


@app.route('/generate', methods=['POST'])
def generate_code():
    question = request.json['question']
    response = llm_chain.run(question)
    code = extract_python_code(response)
    print(code)
    if code is not None:
        return code
    else:
        return response


@app.route('/run', methods=['POST'])
def run_code():
    code = request.json['code']
    stdout, stderr = run_python_code(code)
    return {"stdout": stdout, "stderr": stderr}


# LlamaCpp Application
template = "Question: {question}\n\nAnswer:"
prompt = PromptTemplate(template=template, input_variables=["question"])

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Verbose is required to pass to the callback manager

n_gpu_layers = 200000  # Metal set to 1 is enough.
n_batch = 2048  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path=MODEL,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=4098,
    max_tokens=600,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=True,
)

llm_chain = LLMChain(prompt=prompt, llm=llm)


def extract_python_code(response):
    # Define the regular expression patterns to match the Python code
    pattern = r"```\n(.*?)```"

    # Try each pattern until one matches
    match = re.search(pattern, response, re.DOTALL)
    if match:
        print(f"extracted python code: {match.group(1)}")
        return match.group(1)

    # If no patterns match, return None
    return None


# Running the Flask App
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
