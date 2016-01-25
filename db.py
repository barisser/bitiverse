import os
import pixelwriter as p
import sqlite3

#initial conditions
root_output = {'output': "ea3995f87974c34d8fde332e0194a42ae80d07713c1b36b85869eb4516b48c93:0", 'value': 98000, 'dest_address': '19ytqnQm14XArZRF1ZbmordHg74B56iGxd'}
block_height = 388085
db_name = 'bitistate.db'

create_owners_sql = """
CREATE TABLE owners (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, output \
varchar(255) NOT NULL, address varchar(255) NOT NULL, \
start_block int NOT NULL, end_block int, pixels_owned int);
"""
create_grid_sql = "CREATE TABLE grid (x int, y int, owner_id int NOT NULL, link_id int);"
create_links_sql = """
CREATE TABLE links (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, url int, \
owner_id int NOT NULL, flagged int, publish_block int NOT NULL, publish_tx varchar(255) \
NOT NULL);
"""

def insert_owner(output, address, start_block, pixels_owned, conn):
    sql = """INSERT INTO owners (output, address, start_block, pixels_owned) VALUES \
    ('%s', '%s', %d, %d);""" % (output, address, start_block, pixels_owned)

    c = conn.cursor()
    c.execute(sql)
    c.execute("select id from owners order by id desc limit 1;")
    d = c.fetchall()[0][0]
    return conn, d

def expire_owner(output, end_block, conn=None):
    if conn == None:
        conn = sqlite3.connect(db_name)
    sql = "UPDATE owners set end_block = {0} where \
    output = {1}".format(end_block, output)
    c = conn.cursor()
    c.execute(sql)
    return conn

def init_grid(owner_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "insert into grid (x, y, owner_id) values (%d, %d, %d)"
    for x in range(p.universe_width):
        for y in range(p.universe_height):
            esql = sql % (x, y, owner_id)
            c.execute(esql)
    conn.commit()
    conn.close()

def execute(sql, ret=False):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    if ret:
        d = c.fetchall()
    conn.close()
    if ret:
        return d

def load_owners(end_block=None):
    if end_block == None:
        sql = "select * from OWNERS where end_block is NULL;"
    else:
        sql = "select * from OWNERS where end_block=" + str(end_block) + ";"
    return execute(sql, ret=True)

def load_grid():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "select * from grid;"
    c.execute(sql)
    conn.commit()
    d = c.fetchall()
    conn.close()
    e = [[-1] * p.universe_height] * p.universe_width
    for a in d:
        x = a[0]
        y = a[1]
        owner_id = a[2]
        link_id = a[3]
        e[x][y] = [owner_id, link_id]
    return e

def save_grid(grid_data):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "insert into grid values (%d, %d, %d, %d)"
    for x in range(p.universe_width):
        for y in range(p.universe_height):
            owner_id = grid_data[x][y][0]
            link_id = grid_data[x][y][1]
            esql = sql % (x, y, owner_id, link_id)
            c.execute(esql)
        print str(x) + " / " + str(p.universe_width)
    conn.commit()
    conn.close()

def init_db():
    """
    Inits a new DB at the starting conditions state.
    """
    print "INITIALIZING DB"
    os.system('rm %s' % db_name)
    conn = sqlite3.connect(db_name, isolation_level=None)
    cursor = conn.cursor()

    cursor.execute(create_owners_sql)
    cursor.execute(create_grid_sql)
    cursor.execute(create_links_sql)

    amt = p.universe_width * p.universe_height
    print "Generating Root Owner"
    conn, owner_id = insert_owner(root_output['output'], root_output['dest_address'], \
    block_height, amt, conn)
    conn.close()
    print "Initializing Grid."
    init_grid(owner_id)
