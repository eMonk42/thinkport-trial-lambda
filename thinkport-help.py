import json
import psycopg2

# variables for DB-connection
db_url = "thinkport-companies.cggqco3vithh.us-east-2.rds.amazonaws.com"
db_name = "postgres"
db_user = "thinkport"
db_pwd = "thinkport"
    
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
        
def lambda_handler(event, context):        
    return respond(200, {
            'Welcome_to_my_API': 'Here is a list of routes you can use',
            'get-all-companies': {
                'path': 'url/companies',
                'method': 'GET',
                'query': 'no query',
                'headers': {
                    'Authorization': 'no'
                },
                'body': 'no body',
            },
            'get-single-company': {
                'path': 'url/companies/{id}',
                'method': 'GET',
                'query': 'no',
                'headers': {
                    'Authorization': 'no'
                },
                'body': 'no body',
            },
            'create-new-company': {
                'path': 'url/comnpanies',
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
                'path': 'url/companies/{id}',
                'method': 'DELETE',
                'query': 'no',
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
