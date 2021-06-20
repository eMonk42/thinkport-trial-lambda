import json
import psycopg2
import utils
        
def lambda_handler(event, context):
    conn = psycopg2.connect(host=utils.db_url, dbname=utils.db_name, user=utils.db_user, password=utils.db_pwd)
    connection = utils.Connection(conn)
    path = event['pathParameters']
    #return utils.respond(200, event['pathParameters'])
    #return utils.respond(200, path['id'])
    return utils.respond(200, 'Under construction. Sorry.')
    connection.cursor.execute("""select * from companies where id = %s """, (path['id']))
    return utils.respond(200, "Hello")
    raw = connection.cursor.fetchall()
    return utils.respond(200, raw)
    company = convertToCompany(raw[0])
    connection.conn_db.commit()
    return company