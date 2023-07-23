from flask import Flask, request
from io import StringIO
import sys
from flask_cors import CORS

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Flask App
app = Flask(__name__)
CORS(app)


@app.route('/run', methods=['POST'])
def run_code():
    code = request.json['code']
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    try:
        exec(code)
    except Exception as e:
        print(str(e))
    sys.stdout = old_stdout
    output = redirected_output.getvalue()
    return output


# LlamaCpp Application
template = "Question: {question}\n\nAnswer:"
prompt = PromptTemplate(template=template, input_variables=["question"])

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Verbose is required to pass to the callback manager

n_gpu_layers = 200000  # Metal set to 1 is enough.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="/Users/marconeves/Desktop/desktop/projects/llama.cpp/models/useful_coder/useful-coder-ggml-q4_0.bin",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=2048,
    max_tokens=1500,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=True,
)

llm_chain = LLMChain(prompt=prompt, llm=llm)


@app.route('/generate', methods=['POST'])
def generate_code():
    question = request.json['question']
    response = llm_chain.run(question)
    return response


# Running the Flask App
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
