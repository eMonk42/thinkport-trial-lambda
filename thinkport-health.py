import psycopg2
import utils
        
def lambda_handler(event, context):
    conn = psycopg2.connect(host=utils.db_url, dbname=utils.db_name, user=utils.db_user, password=utils.db_pwd)
    connection = utils.Connection(conn)
    connection.cursor.execute("select now()")
    raw = connection.cursor.fetchall()
    if (raw):
        return utils.respond(200, 'api here. db up and running. connection established.')
    else:
        return utils.respond(500, 'API here. seems like I have no db connection')