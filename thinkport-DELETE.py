import psycopg2
import utils
        
def lambda_handler(event, context):
    conn = psycopg2.connect(host=utils.db_url, dbname=utils.db_name, user=utils.db_user, password=utils.db_pwd)
    connection = utils.Connection(conn)
    path = event['pathParameters']
    connection.cursor.execute("delete from companies where id = "+path['id']+" returning *")
    raw = connection.cursor.fetchall()
    company = utils.convertToCompany(raw[0])
    connection.conn_db.commit()
    return utils.respond(200, company)
