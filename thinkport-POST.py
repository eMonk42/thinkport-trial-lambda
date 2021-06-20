import json
import psycopg2
import utils
        
def lambda_handler(event, context):
    conn = psycopg2.connect(host=utils.db_url, dbname=utils.db_name, user=utils.db_user, password=utils.db_pwd)
    connection = utils.Connection(conn)
    newCompany = json.loads(event['body'])
    if 'name' in newCompany:
        connection.cursor.execute("""insert into companies values(default, %s, %s, %s, %s, %s) returning *""", (newCompany['name'], newCompany['entity'], int(newCompany['worker_count']), int(newCompany['cash']), json.dumps(newCompany['additional_infos'])))
        raw = connection.cursor.fetchall()
        company = utils.convertToCompany(raw[0])
        connection.conn_db.commit()
        return utils.respond(201, company)
    else:
        return utils.respond(204, 'Please provide at least a name for the new company to be created')
