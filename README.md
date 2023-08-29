# baby-code
A simple and 100% Local, Open-Source Code 🐍 Interpreter for 🦙 LLMs

## Baby Llama is:
- [x] powered by [Llama.cpp](https://github.com/ggerganov/llama.cpp)
- [x] extremly SIMPLE & 100% LOCAL
- [x] CROSS-PLATFORM.

https://github.com/itsPreto/baby-code/assets/45348368/a5319303-aa97-4c01-9e91-7d3f03514139

Leveraging [open source gguf models](https://huggingface.co/models?search=gguf) and powered by llama.cpp this project is a humble foundation for enabling LLMs to act as Code Interpreters.

## 🏗️ Architecture (in a nutshell)

- 🖥️ **_Backend_**: Python Flask (CORS for serving both the API and the HTML).
- 🌐 **_Frontend_**: HTML/JS/CSS (I'm not a frontend dev but gave it my best shot-- prolly tons of issues).
- ⚙️ **_Engine_**: Llama.cpp: An inference library for `ggml/gguf` models).
- 🧠 **_Model_**: [GGUF](https://github.com/ggerganov/llama.cpp#description) format (replacing the retired `ggml` format).

## 🦙 Features
- 🎊 Confetti:3
- 💬 Contextual Conversations: Models are augmented with the ongoing context of the conversation-- allowing them to remember and refer back to previous parts of it.
- 🔄 Dynamic Code Interaction: Copy, Diff, Edit, Save and Run the generated Python scripts right from the chat.
- 🐞 Auto-Debugging & 🏃 Auto-Run: Allow the model to automatically debug and execute any attempts at fixing issue on the fly (_it will die trying_).
- 📊 Inference & Performance Metrics: Stay informed about how fast the model is processing your requests and tally the successful vs failed script executions.
- ❓ Random Prompts: Not sure what to ask? Click the "Rand" button to randomly pick from a pre-defined prompt list!

## 🚀 Getting Started ⚠️ IMPORTANT ⚠️ 

- This project is dependent on its submodule `llama.cpp` and relies on its successful build.
- First, clone the repo:

```bash
git clone --recurse-submodules https://github.com/itsPreto/baby-code
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

## 🏗️ Build llama.cpp

In order to build llama.cpp you have three different options.

- Using `make`:
  - On Linux or MacOS:

      ```bash
      make
      ```

  - On Windows:

    1. Download the latest fortran version of [w64devkit](https://github.com/skeeto/w64devkit/releases).
    2. Extract `w64devkit` on your pc.
    3. Run `w64devkit.exe`.
    4. Use the `cd` command to reach the `llama.cpp` folder.
    5. From here you can run:
        ```bash
        make
        ```

- Using `CMake`:

    ```bash
    mkdir build
    cd build
    cmake ..
    cmake --build . --config Release
    ```

### Build Alternatives [Metal](https://github.com/ggerganov/llama.cpp#metal-build), [Intel Mlk](https://github.com/ggerganov/llama.cpp#intel-mkl), [MPI](https://github.com/ggerganov/llama.cpp#mpi-build), [BLIS](https://github.com/ggerganov/llama.cpp/blob/master/docs/BLIS.md) [cuBLAS](https://github.com/ggerganov/llama.cpp#cublas), [clBLAST](https://github.com/ggerganov/llama.cpp#clblast), [OpenBLAS](https://github.com/ggerganov/llama.cpp#openblas), and [hipBLAS](https://github.com/ggerganov/llama.cpp#openblas).

## 💾 Model Download

- [TheBloke/WizardCoder-Python-13B-V1.0-GGUF](https://huggingface.co/TheBloke/WizardCoder-Python-13B-V1.0-GGUF) is a friendly, [gpu] budget model.
- You may also download any other models supported by llama.cpp, of any parameter size of your choosing.
- Keep in mind that the paramters might need to be tuned for your specific case:

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
