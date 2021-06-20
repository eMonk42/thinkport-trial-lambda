import psycopg2
import utils
        
def lambda_handler(event, context):
    conn = psycopg2.connect(host=utils.db_url, dbname=utils.db_name, user=utils.db_user, password=utils.db_pwd)
    connection = utils.Connection(conn)
    result = []
    connection.cursor.execute("select * from companies order by id")
    raw = connection.cursor.fetchall()
    # restructuring of the db-answer
    for line in raw:
        newItem = utils.convertToCompany(line)
        result.append(newItem)
    
    return utils.respond(200, result)