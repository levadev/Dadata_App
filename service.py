import requests

#The functoin requests data from DaData if API token exists
def make_response(settings, data):
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
