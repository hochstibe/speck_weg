# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server File: app.py
#


from server.speck_weg_backend import create_app


if __name__ == '__main__':
    app = create_app()
    app.run()
