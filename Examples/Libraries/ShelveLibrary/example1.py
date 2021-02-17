import shelve

# with shelve.open('spam') as db:
#     db['eggs'] = 'eggs'
#     print(db['something'])

shelve.open("database.db")
