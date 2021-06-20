import utils
        
def lambda_handler(event, context):        
    return utils.respond(200, {
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
