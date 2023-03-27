from flask import Flask , render_template, request, redirect
import pymysql
import pymysql.cursors

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html.jinja")


connection = pymysql.connect(
    host="10.100.33.60",
    user="abattlessmith",
    password="223185349",
    database="abattlessmith_Social",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
    )



@app.route('/post')
def post_feed():
    cursor = connection.cursor("")

    cursor.execute("SELECT * FROM `posts` ORDER BY `Date`")

    results = cursor.fetchall()

    return render_template("posts.html.jinja",post=results )


if __name__ == '__main__':
    app.run(debug=True)