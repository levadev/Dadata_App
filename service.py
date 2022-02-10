import requests

#The functoin requests data from DaData if API token exists
def make_response(settings, data):
    """
    :params settings: dictionary of settings
    :type settings: dict
    :params data: dictionary with parametrs of query
    """
    response = requests.post(settings['URL'], 
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Token {settings['API']}", #public token
        },

        json=data
    )

    response = response.json()
    return response['suggestions']
