from aiohttp import web
from wsplayer import WSPlayer
from wsbrows import WSBrows


def main():
    app = web.Application()
    app.router.add_get('/ws', WSBrows) # browser api
    app.router.add_get('/api', WSPlayer)   # player api

    web.run_app(app, host='127.0.0.1', port=4000)


if __name__ == '__main__':
    main()


