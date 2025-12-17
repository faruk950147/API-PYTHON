# This is the main function that will be called by the server
async def main(scope, receive, send):
    # scope is a dictionary that contains the information about the request
    # it contains the type of the request, the path, the method, the headers, the body, the query parameters, 
    # receive is a coroutine that receives the information about the request
    # send is a coroutine that sends the information about the response
    # assert scope['type'] == 'http' or scope['type'] == 'websocket'
    assert scope['type'] == 'http'

    body = b'Hello, world! & Uvicorn Web Server & FastAPI'
    
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'text/plain'),
            (b'content-length', str(len(body)).encode('utf-8')),
        ],
    })
    
    await send({
        'type': 'http.response.body',
        'body': body,
    })
