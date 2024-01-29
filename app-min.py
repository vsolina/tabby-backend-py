from flask import Flask, request, jsonify
from llama_cpp import Llama

app = Flask(__name__)
llm = Llama(model_path='star-coder-1B-Q5_K_M.gguf', n_ctx=8192, n_gpu_layers=-1)

@app.route('/v1/health')
@app.route('/v1/events', methods=['POST'])
def health_and_events():
    return jsonify({})

@app.route('/v1/completions', methods=['POST'])
def completions():
    segments = request.get_json().get('segments', {})
    prompt = '<fim_prefix>{}<fim_suffix>{}<fim_middle>'.format(segments['prefix'], segments['suffix'])
    return jsonify(llm(prompt, max_tokens=None, temperature=0))

if __name__ == '__main__':
    app.run(threaded=False, processes=1)
