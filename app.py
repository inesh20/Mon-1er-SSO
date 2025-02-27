
from DbHelper import DynamoDBHelper

table = "Users"
dbHelper = DynamoDBHelper(table)

dbHelper.add_user({'email': 'demo', 'password': dbHelper.hash_password('demo'), 'name':'demo'})
result = dbHelper.login('demo', 'demo')
print(result)

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form.get("email")
    password = request.form.get("pswd")
    return dbHelper.login(email, password)

@app.route('/signup', methods=['POST'])
def signup():
    try:
        name = request.form.get("name")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = request.form.get("pswd")
        dbHelper.add_user({'email': email, 'password': dbHelper.hash_password(password), 'name':name, 'mobile': mobile})
        return {"message": "Ajouté avec succès !"}
    except:
        return {"message": "Une erreur est survénue !"}

if __name__ == '__main__':
    app.run("0.0.0.0", port=8081, debug=True)