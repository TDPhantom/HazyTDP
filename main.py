from flask import Flask , render_template, request, redirect,send_from_directory,abort,g
import pymysql
import pymysql.cursors
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'something_random'

@app.route("/")
def index():
    return render_template("home.html.jinja")

class User:
    def __init__(self, id, Username, banned):
        self.is_authenticated = True
        self.is_anonymous = False
        self. is_active = not banned

        self.username = Username
        self.id = id

    def get_id(self):
        return str(self.id)
    

    
def connect_db():
    return pymysql.connect(
    host="10.100.33.60",
    user="abattlessmith",
    password="223185349",
    database="abattlessmith_Social",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
    )
def get_db():
    '''Opens a new database get_db() per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database get_db() at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

@login_manager.user_loader
def user_loader(user_id):
    cursor = get_db().cursor()

    cursor.execute("SELECT * from `Users` WHERE `id` = " + user_id)

    result = cursor.fetchone()

    if result is None:
        return None
    
    return User(result['id'], result['username'], result['banned'])

@app.route('/feed')
@login_required
def post_feed():
    cursor = get_db().cursor("")

    cursor.execute("SELECT * FROM `posts` JOIN `Users` ON `posts`.`user_id`= `Users`.`id` ORDER BY `Date` DESC;")

    results = cursor.fetchall()

    return render_template("posts.html.jinja",posts=results )


@app.route('/sign-out')
def sign_out():
    logout_user()

    return redirect('/sign-in')

@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    if current_user.is_authenticated:
        return redirect('/feed')


    if request.method == "POST":
        cursor = get_db().cursor()

        cursor.execute(f"SELECT * FROM `Users` WHERE `Username` =  '{request.form['Username']}' ")

        result = cursor.fetchone()



        if result is None:
            return render_template("sign_in.html.jinja")
        
        if request.form['Password'] == result['password']:
            user=User(result['id'],result['username'],result['banned'])

            login_user(user)

            return redirect('/feed')

        else:
            return render_template('sign_in.html.jinja')
        




        return request.form

    elif request.method == "GET":
        return render_template("sign_in.html.jinja")

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method =='POST':
        #Handle signup
        cursor = get_db().cursor()

        Profile =request.files['Profile']
       
        file_name = Profile.filename # my_jgp
        
        file_extension = file_name.split('.')[-1]

        if file_extension in ['jpg','jpeg', 'png', 'gif']:
            Profile.save('media/users/' + file_name)

        else:
            raise Exception('Invalid file type')
       
       
       
       
        cursor.execute("""
            INSERT INTO `Users` (`Username`, `display_name`,`email`,`Birthday`,`password`,`bio`,`photo`)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """,(request.form['Username'], request.form['Display Name'], request.form['Email'], request.form['Birthday'], request.form['Password'], request.form['Biography'], file_name))


    


        return redirect('/sign-in')
    elif request.method =='GET':
        return render_template('sign_up.html.jinja')
        
        
        return request.form
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")
    
        



    return render_template("sign_up.html.jinja")

@app.get('/media/<path:path>')
def send_media(path):
    return send_from_directory('media',path)

@app.route('/post', methods=['POST'])
@login_required
def create_post():

    user_id = current_user.id

    cursor = get_db().cursor()

    Profile =request.files['File']
    
    file_name = Profile.filename # my_jgp
    
    file_extension = file_name.split('.')[-1]

    if file_extension in ['jpg','jpeg', 'png', 'gif']:
        Profile.save('media/posts/' + file_name)

    else:
        raise Exception('Invalid file type')

    cursor.execute(
        """INSERT INTO `posts` (`user_id`,`post_image`, `post_text`) VALUES (%s,%s,%s)""",
        (user_id, file_name, request.form['Post'])
    )
    
    return redirect('/feed')

@app.route('/profile/<username>')
def user_profile(username):
    cursor=get_db().cursor()

    cursor.execute("SELECT * FROM `Users` WHERE `Username` = %s",(username))

    result = cursor.fetchone()

    if result is None:
        abort(404)

    cursor.close()
       
    cursor = get_db().cursor()
        
    cursor.execute("SELECT * FROM `posts` WHERE `user_id` = %s",(result['id']))
    
    post_result = cursor.fetchall()


    return render_template("user_profile.html.jinja",user=result)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_status.html.jinja'),404



if __name__ == '__main__':
    app.run(debug=True)