import os
from decouple import config as ENV

DEBUG = True

SECRET_KEY = ENV("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = "postgresql://lupismo_user:slhnTESKYbHWxPFFcFDq9f6MZXfOBvmF@dpg-cpasqvlds78s73d7jr7g-a.oregon-postgres.render.com/lupismo_41i3"

#postgres://lupismo_user:slhnTESKYbHWxPFFcFDq9f6MZXfOBvmF@dpg-cpasqvlds78s73d7jr7g-a.oregon-postgres.render.com/lupismo_41i3



# pegando o nome do caminho absoluto do diretório e concatenando com o diretório uplouds
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}