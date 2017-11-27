# from conf import settings
from cmic import settings

# print(settings.db_type)
if settings.db_type == 'mongodb':
    try:
        from db.backends.mongodb import Client
    except ImportError:
        Client = None
        # from db.backends import mongodb


elif settings.db_type == 'postgresql':
    try:
        from cmic.db.backends.postgresql import Client
    except ImportError:
        Client = None


# db = Client(db_name=settings.db_name, col_name=settings.col_name, host=settings.db_host, port=int(settings.db_port))
db = Client()
