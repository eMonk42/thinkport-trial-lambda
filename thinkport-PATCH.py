import json
import psycopg2
import utils
        
def lambda_handler(event, context):
    conn = psycopg2.connect(host=utils.db_url, dbname=utils.db_name, user=utils.db_user, password=utils.db_pwd)
    connection = utils.Connection(conn)
    company = json.loads(event['body'])
    if 'name' in company:
        connection.cursor.execute("""update companies set name = %s, entity = %s, worker_count = %s, cash = %s, additional_infos = %s where id = %s returning *""", (company['name'], company['entity'], int(company['worker_count']), int(company['cash']), json.dumps(company['additional_infos']), company['id']))
        raw = connection.cursor.fetchall()
        returnedCompany = utils.convertToCompany(raw[0])
        connection.conn_db.commit()
        return utils.respond(200, returnedCompany)
    else:
        return utils.respond(200, 'Plaese provide information inside the request-body')
