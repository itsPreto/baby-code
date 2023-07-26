# 🦙 Baby Code Interpreter
An open-source, locally-run, python code interpreter [(like openAI's GPT-4 Plugin: Code-Interpreter).](https://pub.towardsai.net/gpt-4-code-interpreter-your-magic-wand-for-instant-python-data-visuals-f40fcfb5e39b)

## Baby Code is:
- [x] primarily and mostly for fun, as it is extremely early in development.
- [x] extremly SIMPLE,
- [x] 100% LOCAL &
- [x] CROSS-PLATFORM.

![Screenshot 2023-07-26 at 1 41 33 PM](https://github.com/itsPreto/baby-code/assets/45348368/d895b87b-7d26-44cb-9c1f-05b12f2188ed)

It leverages open source LLMs to interpret user's requests into Python code. 
The service is exposed through a Flask server which receives user's requests, processes them, and returns Python code.

## 🏗️ Architecture (in a nutshell)

- 🖥️ **_Backend_**: Python Flask (CORS for serving both the API and the HTML).
- 🌐 **_Frontend_**: HTML/JS/CSS (The UI was designed 100% to personal liking but open for changes).
- ⚙️ **_Engine_**: Llama.cpp (Inference library for Llama/GGML models).
- 🧠 **_Model_**: Llama-2 (Only models compatible with Llama.cpp).
- ⚖️ **_Arbiter_**: LangChain (Gluing all these components together).
- 🎁 **_Wrapper_**: LlamaCpp (LangChain's wrapper around Llama.cpp for loading the models).

## 🚀 Setup
- Clone the repo:
  
```bash 
git clone https://github.com/itsPreto/baby-interpreter
```

-  Navigate to the project:
  
```bash 
cd baby-interpreter
```

- Install the following libraries (_requirements.txt coming soon..._):
  
```bash 
pip install flask flask_cors subprocess langchain
```
## 🧠 Model Config
This project is configured to use LlamaCpp and load up models for local inference.
Models can be found on HuggingFace and once downloaded you can simply place them in the `\models` folder and update the `MODEL` path variable in `main.py`.
```python 
WIZARD_LM_V2 = "WizardLM-13B-V1.2/WizardLM-13B-V1.2-GGML-q4_0.bin"
USEFUL_CODER = "useful_coder/code-cherryLamma-2/useful-coder-ggml-q4_0.bin"
MODEL = f"./models/{USEFUL_CODER}"
```
## 🏃‍♀️ Run it
- Simply execute: 
```bash 
python main.py 
```

The Flask server will start and listen on port 8000. The server exposes two endpoints ```/generate``` and ```/run.```
## 🌐 Endpoints
- `/generate`: receives a POST request with a user's question in the body. The question is processed by the LLM, and a 
Python code snippet is generated and returned.

- `/run`: receives a POST request with Python code in the body. The code is executed, and the output of the execution 
is returned.
## 🤝 Contributing
  Contributions to this project are welcome. Please create a fork of the repository, make your changes, and submit a pull 
request.
  I'll be creating a few issues for feature tracking soon!!

  
ALSO~~~ If anyone would like to start a Discord channel and help me manage it that would be awesome _(I'm not on it that much)_.
## License
This project is licensed under the MIT License.
