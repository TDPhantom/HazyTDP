from flask import Flask , render_template, request, redirect


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html.jinja")


if __name__ == '__main__':
    app.run(debug=True)
