import shelve
from global_parameters import BASE_DIR
from flask import Flask, g

def create_fake_data():
    # create fake database
    ## save it as json file
    import json
    data = {'first name': 'Anak', 'last_name':'Wannaphaschaiyong'}
    file_name = BASE_DIR / 'Examples\\Libraries\\FlaskRestfulAPI\\database.db'
    with open(file_name, 'w') as f:
        json.dump(data,f)

def init_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open('database.db')

    # print(g._database.keys())
    print(list( db.keys() ))

    keys = list(db.keys())

    import json
    import pickle

    data = {'name':'Anak', 'last name': 'Wannaphaschaiyong'}
    pickle.dump(data, open('test.db', 'wb'))
    x = pickle.load(open('test.db', 'rb'))
    y = shelve.open('test.db')
    print([i for i in x])
    print([i for i in y])
    print()

    # devices = []

    # for key in keys:
    #     devices.append(shelf[key])
    
    # print(devices)


def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app

create_fake_data()
create_app()
