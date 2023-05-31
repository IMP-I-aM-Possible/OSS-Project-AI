from flask import Flask, request, jsonify
import test
import chat

app = Flask(__name__)

@app.route('/ask/<user_input>')
def ask(user_input):
    app.config['JSON_AS_ASCII'] = False    # 한글 깨질때 사용
    return jsonify((test.search(user_input)))

@app.route('/chat/<user_chat>')
def gpt(user_chat):
    app.config['JSON_AS_ASCII'] = False
    return jsonify((chat.gptTest(user_chat)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# flask run --host=0.0.0.0 --port=5000