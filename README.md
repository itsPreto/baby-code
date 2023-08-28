# baby-code
A simple and 100% Local, Open-Source Code 🐍 Interpreter for 🦙 LLMs

## Baby Llama is:
- [x] powered by [Llama.cpp](https://github.com/ggerganov/llama.cpp)
- [x] extremly SIMPLE & 100% LOCAL
- [x] CROSS-PLATFORM.

<img width="1685" alt="Screenshot 2023-08-13 at 1 44 53 PM" src="https://github.com/itsPreto/baby-llama.pycpp/assets/45348368/2dbec8a7-2ab9-448b-9441-92a841ba985a">

Leveraging open source Llama-based models and powered by llama.cpp, this service is exposed through a Flask server which receives user's requests, processes them, and returns Python code.

## 🏗️ Architecture (in a nutshell)

- 🖥️ **_Backend_**: Python Flask (CORS for serving both the API and the HTML).
- 🌐 **_Frontend_**: HTML/JS/CSS (The UI was designed 100% to personal liking but open for changes).
- ⚙️ **_Engine_**: Llama.cpp (Inference library for Llama/GGML models).
- 🧠 **_Model_**: Llama-2 (Only models compatible with Llama.cpp).

## Features

What's New? [(_see old archived repo_)](https://github.com/itsPreto/baby-code/blob/main/README.md)
- 🚀 Performance Boost: By eliminating intermediary layers, the app runs faster and more reliably.\
- 🎨 UI Overhaul: A more elegant and user-friendly design that feels different from any chat application you've used.
- 💬 Contextual Conversations: The model can now remember and refer back to previous parts of the conversation, ensuring you have a coherent chat experience.
- 🔄 Dynamic Code Interaction: Copy, run, or even compare differences between Python code blocks right from the chat.
- 🐞 Auto-Debugging & 🏃 Auto-Run: Errors in the code? The chatbot will let you know. Want to run the code without clicking a button? It can do that too!
- 📊 Inference Metrics: Stay informed about how fast the model is processing your requests.
- 📊 Performance Metrics: Keep a tally of how many scripts run successfully vs how many don't.
- ❓ Random Prompts: Not sure what to ask? Click the "Rand" button for a random prompt!
- 📜 Code Diff Viewer: Select any two generated scripts to perform a fast diff between them.

## 🚀 Setup
- Clone the repo:

```bash
git clone https://github.com/itsPreto/baby-llama.pycpp
```

-  Navigate to the project:

```bash
cd baby-llama.pycpp
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

## 🦙 !IMPORTANT! Build Llama.cpp

- This project is a fork of `Llama.cpp` so it depends on a successful compilation.

- Depending on you OS you have a few options for compiling and building the Llama.cpp library.

- Please refer to their original [build setup](https://github.com/ggerganov/llama.cpp#build)

## 🧠 Model Config
Load up your chosen model `ggml` for local inference using CPU or GPU by simply placing it in the `\models` folder and edit the `baby_code.py` init config below:

```python
if __name__ == '__main__':
    # Run the external command
    subprocess.Popen(["./server", "-m", "models/code_cherry_Llama_q4_0.bin", "-c", "2048", "-ngl", "30"])

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
python3 baby-code/baby_code.py
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
