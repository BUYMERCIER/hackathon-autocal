########################################
from flask import Flask, request
from flask import make_response
import mysql.connector as mariadb
########################################
app = Flask(__name__)

mariadb_connection = mariadb.connect(user='root', database='autocal')
cursor = mariadb_connection.cursor()

###########
@app.route('/')
def index():
    return 'index'

###########
### API ###
###########
@app.route('/api/<uid>/<service>', methods=['GET', 'POST'])
def api(uid=None, service=None):
    """
    query format: requests.post('http://localhost:5000/api/1/taxi',
                                    json={'time': 12, 'location': 'Beijing'})
    parameters:
        time (int)
        location (string)
    """
    if not uid:
        raise Exception("No uid given")
    if not service:
        raise Exception("Sevice not recognised")

    content = request.json
    # fetching the database
    cursor.execute("SELECT first_name,last_name FROM users WHERE id=" + uid)
    custommer = [name for name in cursor]
    first_name = custommer[0][0]


    # taxi
    if service == 'taxi':
        time = str(content['time'])
        location = content['location']
        ret = first_name + ' wants to order a taxi at ' + time
        ret += '<br>location: ' + location
        with open('client.html', 'w') as f:
            print(ret, file=f)
        return ret
    # food_delivery
    if service == 'food_delivery':
        print(content['type'])
        return service

###########
app.run(debug=True, port=5000)

