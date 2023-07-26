# Baby Interpreter Code

## A Python-based service that is:
- simple,
- 100% local &
- cross-platform

It leverages open source LLMs to interpret user's requests into Python code. 
The service is exposed through a Flask server which receives user's requests, processes them, and returns Python code.

## Setup

Install the required libraries to get started (_requirements.txt coming soon..._):

```bash
pip install flask flask_cors subprocess langchain
```

## Model Configuration

This project is configured to use LlamaCpp to load up models for local inference.
Most models can be found on HuggingFace, once downloaded simply move it to the ```\models```
folder and update the `MODEL` path variable in `main.py`.

```python 
WIZARD_LM_V2 = "WizardLM-13B-V1.2/WizardLM-13B-V1.2-GGML-q4_0.bin"
USEFUL_CODER = "useful_coder/code-cherryLamma-2/useful-coder-ggml-q4_0.bin"
MODEL = f"./models/{USEFUL_CODER}"
```

## Running the Application

To run simply execute:

```bash
python app.py
```

The Flask server will start and listen on port 8000. The server exposes two endpoints ```/generate``` and ```/run.```

## Endpoints
/generate
This endpoint receives a POST request with a user's question in the body. The question is processed by the LLM, and a 
Python code snippet is generated and returned.

/run
This endpoint receives a POST request with Python code in the body. The code is executed, and the output of the execution 
is returned.

## Contributing
Contributions to this project are welcome. Please create a fork of the repository, make your changes, and submit a pull 
request.

## License
This project is licensed under the MIT License.
