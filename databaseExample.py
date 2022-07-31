import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (email TEXT, count INTEGER)')

file_name = input('Enter file name: ')
if len(file_name) < 1:
    file_name = 'mbox-short.txt'

fh = open(file_name)

for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    cur.execute('SELECT count FROM Counts WHERE email = ?', (email, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (email, count) values (?, 1)', (email,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 Where email = ?', (email,))
    conn.commit()

sql_string = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sql_string):
    print(str(row[0]), row[1])
cur.close()
