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

# a class for connecting to db
class Connection:
    db_url = "thinkport-companies.cggqco3vithh.us-east-2.rds.amazonaws.com"
    db_name = "postgres"
    db_user = "thinkport"
    db_pwd = "thinkport"

    def __init__(self, conn):
        self.conn_db = conn
        self.cursor = self.conn_db.cursor()
        self.name = "name"
        
    def __del__(self):
        self.cursor.close()
        self.conn_db.close()