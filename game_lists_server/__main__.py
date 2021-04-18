import json
import wsgiref.simple_server

import falcon
import requests

import game_lists_server.controller as controller

app = application = falcon.App()
search = controller.Search()
games = controller.Games()
game = controller.Game()
app.add_route('/games', games)
app.add_route('/game/{guid}', game)

if __name__ == '__main__':
    with wsgiref.simple_server.make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
      

