def responseJson(data: str , message: str = None):
    response = {
        'status': True,
        'message': message,
        'code': 200,
        'data': data
    }
    return response