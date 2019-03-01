from .models import Quote
import urllib.request,json

base_url=app.config['QUOTE_API_BASE_URL']
def get_quote():
    '''
    function that gets the json response to url request
    '''
    get_quote_url=base_url.format()
    with urllib.request.urlopen(get_quote_url) as url:
        get_quote_data=url.read()
        get_quote_response=json.loads(get_quote_data)

        if get_quote_response:
            id=get_quote_response.get('id')
            author=get_quote_response.get('author')

        quote_objects= None
    return source_objects    
