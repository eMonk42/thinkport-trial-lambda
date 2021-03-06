import json
import psycopg2
# psygopg2 is used for the connection to the postgres-DB here

# NOTE: for naming variables/functions I use CamelCase in general
#       but when there is a direct relation to the DB I use snake_case

#
#   Global variables
#

# variables for DB-connection
db_url = "thinkport-companies.cggqco3vithh.us-east-2.rds.amazonaws.com"
db_name = "postgres"
db_user = "thinkport"
db_pwd = "thinkport"

# variables for route paths
getAll = "/companies"
getSingle = "/company"
health = "/health"
help = "/help"

# a class for db-connection with psycopg2. Closes connection automatically when script ends
class Connection:
    def __init__(self, conn):
        self.conn_db = conn
        self.cursor = self.conn_db.cursor()
        
    def __del__(self):
        self.cursor.close()
        self.conn_db.close()

#
# Utility functions
# 

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

#
#   Actual Lambda-Method
#

# lambda handler
# Here are the routes defined, separated by several if-statements
def lambda_handler(event, context):
    conn = psycopg2.connect(host=db_url, dbname=db_name, user=db_user, password=db_pwd)
    connection = Connection(conn)
    
    # GET ALL ROUTE
    # get all db-entrys from the table 'companies' ordered by 'id'. If the table grows big there might be use for LIMIT and OFFSET
    if (event['httpMethod'] == 'GET' and event['path'] == getAll):
        result = []
        connection.cursor.execute("select * from companies order by id")
        raw = connection.cursor.fetchall()
        # restructuring of the db-answer
        for line in raw:
            newItem = convertToCompany(line)
            result.append(newItem)
    
        return respond(200, result)
        
    # GET SINGLE ROUTE
    # used for getting a specific db entry based on it's Id
    elif (event['httpMethod'] == 'GET' and event['path'] == getSingle):
        query = event['queryStringParameters']
        connection.cursor.execute("""select * from companies where id = %s""",(query['id']))
        raw = connection.cursor.fetchall()
        company = convertToCompany(raw[0])
        connection.conn_db.commit()
        return respond(200, company)
        
    # CREATE NEW COMPANY ROUTE
    # used to create a new entry in the db-table 'companies'
    elif (event['httpMethod'] == 'POST' and event['path'] == getSingle):
        newCompany = json.loads(event['body'])
        # only the 'name'-row is required. If the request was sent by the Front-End all unfilled information will also be pre-filled with default-values
        if 'name' in newCompany:
            connection.cursor.execute("""insert into companies values(default, %s, %s, %s, %s, %s) returning *""", (newCompany['name'], newCompany['entity'], int(newCompany['worker_count']), int(newCompany['cash']), json.dumps(newCompany['additional_infos'])))
            raw = connection.cursor.fetchall()
            company = convertToCompany(raw[0])
            connection.conn_db.commit()
            return respond(201, company)
        # if there is no body or nor 'name' key inside it return without creating an entry in the db
        else:
            return respond(204, 'Please provide at least a name for the new company to be created')

    # UPDATE EXISTING COMPANY
    # alters information for an already existent company in the db-table 'companies'.
    elif (event['httpMethod'] == 'PATCH' and event['path'] == getSingle):
        company = json.loads(event['body'])
        # only the 'name'-row is required. If the request was sent by the Front-End all unfilled information will also be pre-filled with default-values
        if 'name' in company:
            connection.cursor.execute("update companies set name = %s, entity = %s, worker_count = %s, cash = %s, additional_infos = %s where id = %s returning *", (company['name'], company['entity'], int(company['worker_count']), int(company['cash']), json.dumps(company['additional_infos']), company['id']))
            raw = connection.cursor.fetchall()
            returnedCompany = convertToCompany(raw[0])
            connection.conn_db.commit()
            return respond(201, returnedCompany)
        # if there is no body or nor 'name' key inside it return without creating an entry in the db
        else:
            return respond(200, 'Plaese provide information inside the request-body')

    # DELETE COMPANY ROUTE
    # used to hard-delete a specific entry from the db-table 'companies' based on it's Id. Also returns the company as a confirmation of success.
    elif (event['httpMethod'] == 'DELETE' and event['path'] == getSingle):
        query = event['queryStringParameters']
        # checks if there is a value in the query that matches the key 'id' and has a value. If not return immediately
        if (len(query['id']) < 1):
            return respond(200, 'Please send the Id of the company to be deleted in the query like this: "?id=42"')
        connection.cursor.execute("delete from companies where id = "+query['id']+" returning *")
        raw = connection.cursor.fetchall()
        company = convertToCompany(raw[0])
        connection.conn_db.commit()
        return respond(200, company)
        
    # HEALTH ROUTE
    # used to check if the API is responsive and if it has a connection to the DB
    elif (event['httpMethod'] == "GET" and event['path'] == health):
        raw = None
        connection.cursor.execute("select now()")
        raw = connection.cursor.fetchall()
        if (raw):
            return respond(200, 'api here. db up and running. connection established.')
        else:
            return respond(500, 'API here. seems like I have no db connection')
            
    # HELP ROUTE
    # this returns information on how to use this API
    elif (event['httpMethod'] == "GET" and event['path'] == help):
        return respond(200, {
            'Welcome_to_my_API': 'Here is a list of routes you can use',
            'get-all-companies': {
                'path': 'url/companies',
                'params': 'no',
                'method': 'GET',
                'query': 'no query',
                'headers': {
                    'Authorization': 'no'
                },
                'body': 'no body',
            },
            'get-single-company': {
                'path': 'url/company',
                'params': 'no',
                'method': 'GET',
                'query': '?id=[id]',
                'headers': {
                    'Authorization': 'no'
                },
                'body': 'no body',
            },
            'create-new-company': {
                'path': 'url/comnpany',
                'params': 'no',
                'method': 'POST',
                'query': 'no query',
                'headers': {
                    'Authorization': 'JWT'
                },
                'body': {
                    'name':'Firmennam',
                    'entity':'Legal Entity',
                    'worker_count':'Mitarbeiteranzahl',
                    'cash':'Stammkapital',
                    'additional_infos': {
                        'rating': 0,
                        'sitz': 'Firmensitz',
                        'your_own_key': 'your_own_value'
                    }
                },
            },
            'delete-company': {
                'path': 'url/comnpany',
                'params': 'no',
                'method': 'DELETE',
                'query': '?id=[id]',
                'headers': {
                    'Authorization': 'JWT'
                },
                'body': {
                    'name':'Firmennam',
                    'entity':'Legal Entity',
                    'worker_count':'Mitarbeiteranzahl',
                    'cash':'Stammkapital',
                    'additional_infos': {
                        'rating': 0,
                        'sitz': 'Firmensitz',
                        'your_own_key': 'your_own_value'
                    }
                },
            },
            'update-company': {
                'path': 'url/comnpany',
                'params': 'no',
                'method': 'PATCH',
                'query': 'no',
                'headers': {
                    'Authorization': 'JWT'
                },
                'body': {
                    'id': 'id',
                    'name':'Firmennam',
                    'entity':'Legal Entity',
                    'worker_count':'Mitarbeiteranzahl',
                    'cash':'Stammkapital',
                    'additional_infos': {
                        'rating': 0,
                        'sitz': 'Firmensitz',
                        'your_own_key': 'your_own_value'
                    }
                },
            },
            'health-check': {
                'path': 'url/health',
                'params': 'no',
                'method': 'GET',
                'query': 'no query',
                'headers': {
                    'Authorization': 'no'
                },
                'body': 'no body',
            },
        })
    # this is when the request doesen' match any route (which should not be able to happen)
    else:
        return respond(501, 'Sorry, I don\'t know what you are looking for...')