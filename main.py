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

    cursor.execute("SELECT * FROM `posts` JOIN `Users` ON `posts`.`user_id`= `Users`.`id` ORDER BY `Date` DESC;")

    results = cursor.fetchall()

    return render_template("posts.html.jinja",posts=results )

@app.route('/sign-in')
def sign_in():
    return render_template("sign_in.html.jinja")

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method =='POST':
        #Handle signup
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO `users` (`username`, `display_name`,`email`,`birthday`,`password`,`bio`,`photo)
            VALUES(%s,%s,%s,%s,%s,%s,%s,)
        """,[])
        
        
        return request.form
    elif request.method == 'GET':
        return render_template("Sign_up.html.jinja")
    
        



    return render_template("sign_up.html.jinja")



if __name__ == '__main__':
    app.run(debug=True)