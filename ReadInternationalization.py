import sys, sqlite3

filepointer = open('de-de.lang', "r")
schema = 'de-de'

database_connection = sqlite3.connect('faust_bot.db')
cursor = database_connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS i18n (ident TEXT , lang TEXT, longText TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS explain(ident TEXT  PRIMARY KEY, longText INT)''')
database_connection.commit()

cursor = database_connection.cursor()
cursor.execute('DELETE FROM i18n WHERE lang = ?', (schema,))
database_connection.commit()

ident = None
long = None
switch = True
cursor = database_connection.cursor()
for line in filepointer:
    if(switch):
        ident = line.rstrip()
    else:
        long = line.rstrip()
        if 'en-us' != "explain":
            print("Blatsch")
            cursor.execute("INSERT INTO i18n(ident, lang, longText) VALUES(?,?,?)",(ident, schema, long,))
            database_connection.commit()
        else:
            cursor.execute("INSERT INTO explain(ident, longText) VALUES(?,?)", (ident, long,))
            database_connection.commit()
    switch = False if switch else True
database_connection.close()