from flask import Flask
from flask import request, jsonify, abort, make_response
from gensim.summarization.summarizer import summarize

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return Response(response="\n", status=200)

@app.route('/invocations', methods=['POST'])
def lambda_handler():
    data = request.data
    if not data:
        abort(make_response(jsonify(message="Request must have raw text"), 400))
    summary = summarize(data)
    return jsonify({
        'summary': summary
    })


def start_server():
    logging.info('Starting the inference server with {} workers.'.format(model_server_workers))

    # link the log streams to stdout/err so they will be logged to the container logs
    subprocess.check_call(['ln', '-sf', '/dev/stdout', '/var/log/nginx/access.log'])
    subprocess.check_call(['ln', '-sf', '/dev/stderr', '/var/log/nginx/error.log'])

    nginx = subprocess.Popen(['nginx', '-c', '/opt/program/nginx.conf'])
    gunicorn = subprocess.Popen(['gunicorn',
                                 '--timeout', str(model_server_timeout),
                                 '-k', 'gevent',
                                 '-b', 'unix:/tmp/gunicorn.sock',
                                 '-w', str(model_server_workers),
                                 'wsgi:app'])

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(nginx.pid, gunicorn.pid))

    # If either subprocess exits, so do we.
    process_ids = {nginx.pid, gunicorn.pid}
    while True:
        pid, _ = os.wait()
        if pid in process_ids:
            break

    sigterm_handler(nginx.pid, gunicorn.pid)
    logging.info('Inference server exiting')


# The main routine just invokes the start function.
if __name__ == '__main__':
    start_server()
