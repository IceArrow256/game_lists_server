import json
import wsgiref.simple_server

import falcon
import requests

import game_lists_server.controller as controller

app = application = falcon.App()
search = controller.Search()
game = controller.Game()
search = controller.Search()
app.add_route('/game/{id}', game)
app.add_route('/search', search)

if __name__ == '__main__':
    with wsgiref.simple_server.make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
      

