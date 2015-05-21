import webapp2


routes = [
    (r'/', 'handlers.troll_bot_handler.TrollBotHandler')
]

config = {}

app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8001')


if __name__ == '__main__':
    main()