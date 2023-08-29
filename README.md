# baby-code
A simple and 100% Local, Open-Source Code 🐍 Interpreter for 🦙 LLMs

## Baby Llama is:
- [x] powered by [Llama.cpp](https://github.com/ggerganov/llama.cpp)
- [x] extremly SIMPLE & 100% LOCAL
- [x] CROSS-PLATFORM.

<img width="1685" alt="Screenshot 2023-08-13 at 1 44 53 PM" src="https://github.com/itsPreto/baby-llama.pycpp/assets/45348368/2dbec8a7-2ab9-448b-9441-92a841ba985a">

Leveraging (open source gguf models)[https://huggingface.co/models?search=gguf] and powered by llama.cpp this project is a humble foundation for enabling LLMs to act as Code Interpreters.

## 🏗️ Architecture (in a nutshell)

- 🖥️ **_Backend_**: Python Flask (CORS for serving both the API and the HTML).
- 🌐 **_Frontend_**: HTML/JS/CSS (I'm not a frontend dev but gave it my best shot-- prolly tons of issues).
- ⚙️ **_Engine_**: Llama.cpp: An inference library for `ggml/gguf` models).
- 🧠 **_Model_**: (GGUF)[https://github.com/ggerganov/llama.cpp#description] format (replacing the retired `ggml` format).

## 🦙 Features
- 🎊 Confetti:3
- 💬 Contextual Conversations: Models are augmented with the ongoing context of the conversation-- allowing them to remember and refer back to previous parts of it.
- 🔄 Dynamic Code Interaction: Copy, Diff, Edit, Save and Run the generated Python scripts right from the chat.
- 🐞 Auto-Debugging & 🏃 Auto-Run: Allow the model to automatically debug and execute any attempts at fixing issue on the fly (_it will die trying_).
- 📊 Inference & Performance Metrics: Stay informed about how fast the model is processing your requests and tally the successful vs failed script executions.
- ❓ Random Prompts: Not sure what to ask? Click the "Rand" button to randomly pick from a pre-defined prompt list!

## 🚀 Getting Started
- Clone the repo:

```bash
git clone https://github.com/itsPreto/baby-code
```

-  Navigate to the llama.cpp submodule:

```bash
cd baby-code/llama.cpp
```

- Install the required libraries:

```bash
pip install -r requirements.txt
```

- Then repeat the same for the root project:
```bash
cd baby-code && pip install -r requirements.txt
```

## 💾 Model Download

- The 7B Llama-2 based model [TheBloke/WizardCoder-Python-13B-V1.0-GGUF](https://huggingface.co/TheBloke/WizardCoder-Python-13B-V1.0-GGUF) is a model fine-tuned by [a kind redditor](https://www.reddit.com/r/LocalLLaMA/comments/156htzy/i_made_llama2_7b_into_a_really_useful_coder/)
- You may also download any other models supported by llama.cpp, of any parameter size of your choosing.
- Keep in mind that the paramters might need to be tuned for your specific case:

## ⚠️ IMPORTANT ⚠️ 

- This project is dependent on its submodule `llama.cpp` and relies on its successful build.

- Please refer to their original [build setup](https://github.com/ggerganov/llama.cpp#build) to setup on your specific OS.

## 🧠 Model Config
Load up your chosen model `gguf` for local inference using CPU or GPU by simply placing it in the `llama.cpp/models` folder and edit the `baby_code.py` init config below:

```python
if __name__ == '__main__':
    # Run the external command
    server_process = subprocess.Popen(
        ["./llama.cpp/server", "-m", "./llama.cpp/models/wizardcoder-python-13b-v1.0.Q5_K_M.gguf", "-c", "1024",
         "-ngl", "1", "--path", "."])
    # Pause for 5 seconds
    time.sleep(5)
    app.run(args.host, port=args.port)
```

You may also want to customize & configure the flask server at the top of the file, like so:

```python
parser = argparse.ArgumentParser(description="An example of using server.cpp with a similar API to OAI. It must be used together with server.cpp.")
parser.add_argument("--stop", type=str, help="the end of response in chat completions(default: '</s>')", default="</s>")
parser.add_argument("--llama-api", type=str, help="Set the address of server.cpp in llama.cpp(default: http://127.0.0.1:8080)", default='http://127.0.0.1:8080')
parser.add_argument("--api-key", type=str, help="Set the api key to allow only few user(default: NULL)", default="")
parser.add_argument("--host", type=str, help="Set the ip address to listen.(default: 127.0.0.1)", default='127.0.0.1')
parser.add_argument("--port", type=int, help="Set the port to listen.(default: 8081)", default=8081)
```

## 🏃‍♀️ Run it
- From the project `root` simply run:
```bash
python3 baby_code.py
```

The `server.cpp` will be served to `http://127.0.0.1:8080/` by default, while the the Flask (`baby_code.py`) currently listens on port 8081.

## 🌐 Endpoints

-   **POST** `/completion`: Given a prompt, it returns the predicted completion.

    *Options:*

    `temperature`: Adjust the randomness of the generated text (default: 0.8).

    `top_k`: Limit the next token selection to the K most probable tokens (default: 40).

    `top_p`: Limit the next token selection to a subset of tokens with a cumulative probability above a threshold P (default: 0.9).

    `n_predict`: Set the number of tokens to predict when generating text. **Note:** May exceed the set limit slightly if the last token is a partial multibyte character. When 0, no tokens will be generated but the prompt is evaluated into the cache. (default: 128, -1 = infinity).

    `n_keep`: Specify the number of tokens from the initial prompt to retain when the model resets its internal context.
    By default, this value is set to 0 (meaning no tokens are kept). Use `-1` to retain all tokens from the initial prompt.

    `stream`: It allows receiving each predicted token in real-time instead of waiting for the completion to finish. To enable this, set to `true`.

    `prompt`: Provide a prompt. Internally, the prompt is compared, and it detects if a part has already been evaluated, and the remaining part will be evaluate. A space is inserted in the front like main.cpp does.

    `stop`: Specify a JSON array of stopping strings.
    These words will not be included in the completion, so make sure to add them to the prompt for the next iteration (default: []).

    `tfs_z`: Enable tail free sampling with parameter z (default: 1.0, 1.0 = disabled).

    `typical_p`: Enable locally typical sampling with parameter p (default: 1.0, 1.0 = disabled).

    `repeat_penalty`: Control the repetition of token sequences in the generated text (default: 1.1).

    `repeat_last_n`: Last n tokens to consider for penalizing repetition (default: 64, 0 = disabled, -1 = ctx-size).

    `penalize_nl`: Penalize newline tokens when applying the repeat penalty (default: true).

    `presence_penalty`: Repeat alpha presence penalty (default: 0.0, 0.0 = disabled).

    `frequency_penalty`: Repeat alpha frequency penalty (default: 0.0, 0.0 = disabled);

    `mirostat`: Enable Mirostat sampling, controlling perplexity during text generation (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0).

    `mirostat_tau`: Set the Mirostat target entropy, parameter tau (default: 5.0).

    `mirostat_eta`: Set the Mirostat learning rate, parameter eta (default: 0.1).

    `seed`: Set the random number generator (RNG) seed (default: -1, -1 = random seed).

    `ignore_eos`: Ignore end of stream token and continue generating (default: false).

    `logit_bias`: Modify the likelihood of a token appearing in the generated text completion. For example, use `"logit_bias": [[15043,1.0]]` to increase the likelihood of the token 'Hello', or `"logit_bias": [[15043,-1.0]]` to decrease its likelihood. Setting the value to false, `"logit_bias": [[15043,false]]` ensures that the token `Hello` is never produced (default: []).

-   **POST** `/tokenize`: [NOT YET EXPOSED THROUGH baby-code.py] Tokenize a given text.

    *Options:*

    `content`: Set the text to tokenize.

    Note that the special `BOS` token is not added in fron of the text and also a space character is not inserted automatically as it is for `/completion`.

-   **POST** `/embedding`: [NOT YET EXPOSED THROUGH baby-code.py] Generate embedding of a given text just as [the embedding example](../embedding) does.

    *Options:*

    `content`: Set the text to process.

-   **POST** `/run_python_code`: Attempt to sanitize, format and execute the python code provided. Yields the `stderr/stdout`.

    *Options:*

    `code`: Python code (most likely generated by the llm).

## 🤝 Contributing
> Contributions to this project are welcome. Please create a fork of the repository, make your changes, and submit a pull
request.
> I'll be creating a few issues for feature tracking soon!!
>
> ALSO~ If anyone would like to start a Discord channel and help me manage it that would be awesome
>
> _(I'm not on it that much)_.

## License
This project is licensed under the MIT License.
