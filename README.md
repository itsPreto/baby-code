# 🦙 Baby Code Interpreter
An open-source, locally-run, python code interpreter [(like openAI's GPT-4 Plugin: Code-Interpreter)](https://pub.towardsai.net/gpt-4-code-interpreter-your-magic-wand-for-instant-python-data-visuals-f40fcfb5e39b) (though not as capable, _for now_ _🚀_)

## Baby Code is:
- [x] primarily and mostly for fun, as it is extremely early in development.
- [x] extremly SIMPLE,
- [x] 100% LOCAL &
- [x] CROSS-PLATFORM.

<img width="1004" alt="Screenshot 2023-07-30 at 10 46 07 PM" src="https://github.com/itsPreto/baby-code/assets/45348368/0237f891-be3d-473e-a488-39c5b529da7f">

It leverages open source LLMs to interpret user's requests into Python code. 
The service is exposed through a Flask server which receives user's requests, processes them, and returns Python code.

## 🏗️ Architecture (in a nutshell)

- 🖥️ **_Backend_**: Python Flask (CORS for serving both the API and the HTML).
- 🌐 **_Frontend_**: HTML/JS/CSS (The UI was designed 100% to personal liking but open for changes).
- ⚙️ **_Engine_**: Llama.cpp (Inference library for Llama/GGML models).
- 🧠 **_Model_**: Llama-2 (Only models compatible with Llama.cpp).

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
- You may also download any other models supported by llama.cpp, of any parameter size of your choosing.
- Keep in mind that the paramters might need to be tuned for your specific case:

## Running it (TODO)

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
>>>>>>> origin/develop
