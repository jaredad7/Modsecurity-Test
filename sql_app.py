
import os, hashlib, psycopg2
from flask import Flask, request, render_template
from time import gmtime, strftime

app = Flask(__name__)
app.config.from_object(__name__)
port = int(os.getenv("PORT", 80))

# Homepage
@app.route("/")
def index():
    return render_template('home.html')


#Save a string to the database
@app.route("/save/", methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        now = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        unique_id = str(hashlib.sha224(now.encode('utf-8')).hexdigest())
        save_str = "INSERT INTO inputs VALUES('" + unique_id + "', '" + str(request.form['input']) + "');" #SQL Injection vulnerable
        conn = psycopg2.connect(dbname = "test", user = "postgres", host = "localhost", password = "password")
        cur = conn.cursor()
        cur.execute(save_str)
        conn.commit()
        cur.execute("SELECT * FROM inputs;")
        data = cur.fetchall()
        cur.close()
        conn.close()
        print(data)
        return render_template('home.html', hist = data)
    else:
        return "<p>Error<p>"


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=port)

#Running
#export FLASK_APP=sql_app.py
#/usr/local/bin/flask run
