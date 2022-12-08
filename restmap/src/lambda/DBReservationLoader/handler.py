headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9)', 'Accept': 'text/html,application/xhtml+xml', 'Accept-Language': 'en-US', 'Cache-Control': 'cache-max-age=0'}

status = r.status_code

# Handle response type conversion

output = r.text
body = 

success_flag = True


if :

    
    body = json.dumps()
    
    response = {
        'statusCode': ,
        'body': body 
    }
else:
    error_response_switch = {
        5: "Server side error",
        4: "Client error",
        3: "Redirection",
    }
    error_response = f"{error_response_switch[int(str(error_code)[0])]}"
    response = {
        'statusCode': ,
        'error': error_response
    }

return response  