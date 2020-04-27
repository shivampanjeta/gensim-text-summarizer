from flask import Flask
from flask import request, jsonify, abort, make_response
from gensim.summarization.summarizer import summarize

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return Response(response="\n", status=200)

@app.route('/summarize', methods=['POST'])
def lambda_handler():
    data = request.data
    if not data:
        abort(make_response(jsonify(message="Request must have raw text"), 400))
    summary = summarize(data)
    return jsonify({
        'summary': summary
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
