from waitress import serve
from SGC.wsgi import application  

if __name__ == '__main__':
    #serve(application, host='127.0.0.1', port=8000)
    serve(application, host='127.0.0.1', port=8000, threads=4, _quiet=False)
