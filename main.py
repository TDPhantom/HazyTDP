from flask import Flask , render_template, request, redirect
import pymysql
import pymysql.cursors
from flask_login import LoginManager

login_manager = LoginManager

app = Flask(__name__)
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("home.html.jinja")

class User:
    def __init__(self, id, Username, banned):
        self.is_authenticated = True
        self.is_anonymous = False
        self. is_active = not banned

        self.user = Username
        self.id = id

    def get_id(self):
        return str(self.id)
    

    

connection = pymysql.connect(
    host="10.100.33.60",
    user="abattlessmith",
    password="223185349",
    database="abattlessmith_Social",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
    )
@login_manager.user_loader
def user_loader(user_id):
    cursor = connection.cursor()

    cursor.execute("SELECT * from `Users` WHERE `id` = " + user_id)

    result = cursor.fetchone()

    if result is None:
        return None
    
    return User(result['id'], result['Username'], result['banned'])

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

        Profile =request.files['Profile']
       
        file_name = Profile.filename # my_jgp
        
        file_extension = file_name.split('.')[-1]

        if file_extension in ['jpg','jpeg', 'png', 'gif']:
            Profile.save('media/users' + file_name)

        else:
            raise Exception('Invalid file type')
       
       
       
       
        cursor.execute("""
            INSERT INTO `Users` (`username`, `display_name`,`email`,`Birthday`,`password`,`bio`,`photo`)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """,(request.form['Username'], request.form['Display Name'], request.form['Email'], request.form['Birthday'], request.form['Password'], request.form['Biography'], file_name))


        return redirect('/posts')
    elif request.method =='GET':
        return render_template('sign_up.html.jinja')
        
        
        return request.form
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")
    
        



    return render_template("sign_up.html.jinja")



if __name__ == '__main__':
    app.run(debug=True)