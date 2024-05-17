from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/device-editor')
def device_editor():
    return render_template('device_editor.html')

@app.route('/photo-editor')
def photo_editor():
    return render_template('photo_editor.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
