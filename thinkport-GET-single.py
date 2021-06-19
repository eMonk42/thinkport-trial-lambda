import json
import psycopg2
# variables for DB-connection
db_url = "thinkport-companies.cggqco3vithh.us-east-2.rds.amazonaws.com"
db_name = "postgres"
db_user = "thinkport"
db_pwd = "thinkport"

# converts the return of a db-query into a company-object which can be send back to the client.
def convertToCompany(data):
    return {
        'id': data[0],
        'name': data[1],
        'entity': data[2],
        'worker_count': data[3],
        'cash': data[4],
        'additional_infos': data[5]
    }
    
# a simple constructor for the http response. It takes in a statusCode and a payload. 
# Also applies CORS-headers.
def respond(statusCode, data):
    return {
            'statusCode': statusCode,
            'body': json.dumps(data),
            'headers': {
                'Access-Control-Allow-Origin': 'https://musing-einstein-50e174.netlify.app',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,PATCH,DELETE,POST',
                "Access-Control-Allow-Credentials" : 'true'
            }
    }

class Connection:
    def __init__(self, conn):
        self.conn_db = conn
        self.cursor = self.conn_db.cursor()
        self.name = "name"
        
    def __del__(self):
        self.cursor.close()
        self.conn_db.close()
        
def lambda_handler(event, context):
    conn = psycopg2.connect(host=db_url, dbname=db_name, user=db_user, password=db_pwd)
    connection = Connection(conn)
    path = event['pathParameters']
#   return respond(200, event['pathParameters'])
    #return respond(200, json.dumps(path['id']))
    connection.cursor.execute("select * from companies where id = "+json.dumps(path['id']))
    return respond(200, "Hello")
    raw = connection.cursor.fetchall()
    return respond(200, raw)
    company = convertToCompany(raw[0])
    connection.conn_db.commit()
    return company
