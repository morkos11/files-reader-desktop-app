import sqlite3

def special_file_export(name,id,phone,first_name,last_name,email,birthday,gender,locale,link):
    name = name+'.db'
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS special_facebookusers (id INT PRIMARY KEY , phone VARCHAR(25), first_name VARCHAR(35), last_name VARCHAR(35), email VARCHAR(125),birthday VARCHAR(35),gender VARCHAR(25),locale VARCHAR(35),link VARCHAR(150))')
    conn.commit()
    conn.close()
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute('INSERT INTO special_facebookusers VALUES (?,?,?,?,?,?,?,?,?)',(id,phone,first_name,last_name,email,birthday,gender,locale,link))
    conn.commit()
    conn.close()

def file_export(name,id,phone,first_name,last_name,email,birthday,gender,locale,hometown,location,link):
    name = name+'.db'
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS facebookusers (id INT PRIMARY KEY , phone VARCHAR(25), first_name VARCHAR(35), last_name VARCHAR(35), email VARCHAR(125),birthday VARCHAR(35),gender VARCHAR(25),locale VARCHAR(35),hometown VARCHAR(35),location VARCHAR(35),link VARCHAR(150))')
    conn.commit()
    conn.close()
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute('INSERT INTO facebookusers VALUES (?,?,?,?,?,?,?,?,?,?,?)',(id,phone,first_name,last_name,email,birthday,gender,locale,hometown,location,link))
    conn.commit()
    conn.close()