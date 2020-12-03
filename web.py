from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("image_process.html")

if __name__ == "__main__":
    app.run()