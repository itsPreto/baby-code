# 🦙 Baby Code Interpreter
An open-source, locally-run, python code interpreter [(like openAI's GPT-4 Plugin: Code-Interpreter)](https://pub.towardsai.net/gpt-4-code-interpreter-your-magic-wand-for-instant-python-data-visuals-f40fcfb5e39b) (though not as capable, _for now_ _🚀_)

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
git clone https://github.com/itsPreto/baby-code
```

-  Navigate to the project:
  
```bash 
cd baby-code
```

- Install the required libraries:
  
```bash 
pip install -r requirements.txt
```

## 💾 Model Download

- With everything installed you just need a model.
- The 7B Llama-2 based model [TheBloke/llama2-7b-chat-codeCherryPop-qLoRA-GGML](https://huggingface.co/TheBloke/llama2-7b-chat-codeCherryPop-qLoRA-GGML) is a model fine-tuned by [a kind redditor](https://www.reddit.com/r/LocalLLaMA/comments/156htzy/i_made_llama2_7b_into_a_really_useful_coder/)
- You may also download any other models supported by llama.cpp (_llama-cpp-python_), of any parameter size of your choosing.
- Keep in mind that the paramters might need to be tuned for your specific case:

```python
model_path=MODEL,
n_gpu_layers=n_gpu_layers,
n_batch=n_batch,
n_ctx=4098,
max_tokens=600,
f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
callback_manager=callback_manager,
verbose=True,
```

## 🧠 Model Config
This project is configured to use [llama.cpp](https://github.com/ggerganov/llama.cpp) to load up models for local inference using CPU or GPU.
Once your model is downloaded you can simply place it in the `\models` folder and update the `MODEL` path variable in `main.py`.
```python 
WIZARD_LM_V2 = "WizardLM-13B-V1.2/WizardLM-13B-V1.2-GGML-q4_0.bin"
USEFUL_CODER = "code_cherry_Llama_q4_0.bin"
MODEL = f"models/{USEFUL_CODER}"
```
## 🏃‍♀️ Run it
- To start the backend simply run: 
```bash 
python main.py 
```

The Flask server will start and listen on port 8000. The server exposes two endpoints `/generate` and `/run.`
## 🌐 Endpoints
- `/generate`: receives a POST request with a user's question in the body. The question is processed by the LLM, and a 
Python code snippet is generated and returned.

- `/run`: receives a POST request with Python code in the body. The code is executed, and the output of the execution 
is returned.

## 🤝 Contributing
> Contributions to this project are welcome. Please create a fork of the repository, make your changes, and submit a pull 
request.
> I'll be creating a few issues for feature tracking soon!!
> 
> ALSO~~~ If anyone would like to start a Discord channel and help me manage it that would be awesome
> 
> _(I'm not on it that much)_.
## License
This project is licensed under the MIT License.
