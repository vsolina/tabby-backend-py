# Tabby server in 20 lines of python

Tabby is a self-hosted OSS AI coding assistant\
I use it every day and you should too\
Please support the authors https://github.com/TabbyML/tabby

The problem I have with it is the complexity of its backend\
So I reverse engineered it in python (without reading the codebase, some bugs are likely)

## Installation
Clone this repo and install 2 dependencies:
```sh
git clone https://github.com/vsolina/tabby-backend-py.git
cd tabby-backend-py
# optionally create venv:
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Download the model you want to use, e.g. 🤗:
```sh
wget https://huggingface.co/TabbyML/StarCoder-1B/resolve/main/ggml/q8_0.v2.gguf
```
Update model path in app.py (literally called `model_path` in `model_config`)\
*Use relative or absolute path to the model (no shell expansion, e.g.: ~/)*

Run the service:
```sh
python app.py

# OR if you want to customize the port, host
flask run --port 8080 --host 0.0.0.0
```
Install Tabby Extension and update server URL in the Extension configuration:\
https://tabby.tabbyml.com/docs/extensions/

Customization:
- All configuration is defined at the beginning of app.py
- Model used must support FIM (StableCode, StarCoder, CodeLlama, etc.)
- You can provide more params to Llama class by extending `model_config`
- Same for generator config
- Available options here https://llama-cpp-python.readthedocs.io/en/latest/api-reference/

Notes:
- Some bugs are ~~possible~~(ehm)likely, use at your own risk (or fix and open a PR)
- Missing language customizations (Stop Words, Repository Context), but completion still works well
- Endpoint /events is not really implemented (mostly not essential)
- q5_K_M quantized model versions are recommended for best performance vs quality loss ratio
- If you have specific HW acceleration considerations install llama-cpp-python this way:\
https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#installation-with-specific-hardware-acceleration-blas-cuda-metal-etc
- This guy is awesome https://huggingface.co/TheBloke take a look at his quantized model selection

Long live the king Georgi https://github.com/ggerganov

## Start unnecessary Rant 👴 🤌 ☁️
We must fight the complexity demon because it wins by default\
I believe software should be anticomplex

Original TabbyML server implementation (v0.7.0)\
has 530 dependencies (https://github.com/TabbyML/tabby/blob/main/Cargo.lock) \
has 7178 lines of Rust code in 73 files across 9 crates \
uses 3 languages (Rust, Python, C++) according to github

This implementation has\
2 (first level) dependencies \
20 lines of code in one file (app-min.py), 671 bytes

simple is better than complex is better than complicated

When I can read it\
I can understand it\
I can fix it

That makes it antifragile and easy to maintain

Rant over, have a great day
