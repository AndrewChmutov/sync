from sync.app import App

_app = App(ssl_certfile="../cert/cert.pem", ssl_keyfile="../cert/key.pem")
app = _app._app

if __name__ == "__main__":
    _app.run()("sync.main:app")
