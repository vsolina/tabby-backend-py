from flask import Flask, request, jsonify
from llama_cpp import Llama
from threading import Lock


model_config = {
    'model_path': 'star-coder-1B-Q5_K_M.gguf',
    'n_ctx': 8192, ## Depends on the model
    'n_gpu_layers': -1, ## Run all on GPU
}
generator_config = {
    'temperature': 0,
    'max_tokens': 256,
}

app = Flask(__name__)
llm = Llama(**model_config)
model_lock = Lock()

@app.route('/v1/health')
def health():
    # Original structure looks like this:
    # {
    #     "model": "TabbyML/StarCoder-1B",
    #     "device": "cuda",
    #     "arch": "x86_64",
    #     "cpu_info": "...",
    #     "cpu_count": 16,
    #     "cuda_devices": [
    #         ...
    #     ],
    #     "version": {
    #         ...
    #     }
    # }
    # But since that part is completely non-functional, just to prove the point we return:
    return jsonify({'irrelevant': 'nonfunctional metadata'})

def _complete(lang, prefix, suffix):
    # Use model lock to ensure no parallel execution
    with model_lock:
        prompt = '<fim_prefix>{}<fim_suffix>{}<fim_middle>'.format(prefix, suffix)
        res = llm(prompt, **generator_config)
        return {
            'id': res['id'], 
            'choices': [{'index': choice['index'], 'text': choice['text']} for choice in res['choices']]
        }

@app.route('/v1/completions', methods=['POST'])
def completions():
    data = request.get_json()
    lang = data.get('language')  # Not really used for now
    prefix = data.get('segments', {}).get('prefix', '')
    suffix = data.get('segments', {}).get('suffix', '')

    return jsonify(_complete(lang, prefix, suffix))

@app.route('/v1/events', methods=['POST'])
def events():
    # No idea what this one does, when I figure it out I'll implement it
    return jsonify({})


if __name__ == '__main__':
    app.run(threaded=True)
