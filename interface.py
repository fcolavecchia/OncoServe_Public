import os, shutil
from flask import Flask
from flask import render_template, redirect, request, json, jsonify
from learning import analyzer
from werkzeug.utils import secure_filename

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config.update(
    DEBUG=True,
    SERVER_NAME="localhost:5000",
    UPLOAD_FOLDER=os.path.join(APP_ROOT, 'static/uploads')
)

@app.route('/')
def index():
    # Deletes previously uploaded files on refresh
    for files in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], files)
        if os.path.isfile(filepath):
            os.unlink(filepath)
    return render_template('index.html')

@app.route('/serving', methods=['POST'])
def serving():
    try:
        data = request.files['file']
        filename = str(secure_filename(data.filename))
        data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        model = request.form.get('model')
        response = analyzer(data, model)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run()
