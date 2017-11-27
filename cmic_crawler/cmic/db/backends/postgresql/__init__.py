
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Sequence, Boolean, Text, Date
from sqlalchemy.types import PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY

# for show create
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql

# engine = create_engine("postgresql+psycopg2://r7:lulu0501@/", echo=True, pool_size=0)

base_article = declarative_base()


class Comicbook(base_article):
    __tablename__ = 'comic_record_curhash'
    no = Column(Integer, Sequence('comic_seq'), primary_key=True)
    comic_id = Column(String)
    comic_hui = Column(Integer)
    comic_img_order = Column(Integer)
    web_path_sha1 = Column(String, unique=True)
    # content = Column(Text)
    # tags = Column(ARRAY(PickleType))
    web_path = Column(String)
    file_hash = Column(String)
    local_path = Column(String)
    # author = Column(String, nullable=True)
    create_date = Column(Date, nullable=True)
    update_date = Column(Date, nullable=True)


print(CreateTable(Comicbook.__table__).compile(dialect=postgresql.dialect()))

#
# class MiniK(base_minik):
#     __tablename__ = 'minik'
#     id = Column(Integer, Sequence('minik_seq'), primary_key=True)
#     mac = Column(String, unique=True)
#     phone = Column(String)
#     user_id = Column(String)
#     password = Column(String)
#     type = Column(String)
#     red_control_pad = Column(ARRAY(PickleType))


class Client:

    def __init__(self):
        self.con, self.meta = self.connect('r7', 'lulu0501', 'cmic')
        if not self.con.has_table(Comicbook.__tablename__):
            base_article.metadata.create_all(self.con)

        self.Session = sessionmaker(bind=self.con)

    # def get_session(self):
    #     session = self.Session()
    #     return session
    #
    # def find_article(self, search_ip):
    #     session = self.get_session()
    #     proxy = session.query(Article).filter_by(ip=search_ip).first()
    #     session.close()
    #     return proxy
    #
    # def add_article(self, article):
    #     session = self.get_session()
    #     session.add(article)
    #     session.commit()
    #     session.close()
    #
    # def check_article_exist(self, article_id):
    #     session = self.get_session()
    #     res_article = session.query(Article).filter_by(article_id=article_id).first()
    #     session.close()
    #     if res_article:
    #         return True
    #     else:
    #         return False
    #
    # def get_all_proxy(self):
    #     session = self.get_session()
    #     proxy_list = session.query(Article).all()
    #     session.close()
    #     if len(proxy_list) > 0:
    #         return proxy_list
    #
    # def update_proxy(self, article):
    #     session = self.get_session()
    #     old_minik = session.query(Article).filter_by(ip=article.ip).first()
    #
    #     for k, v in old_minik.__dict__.items():
    #         if k != "_sa_instance_state":
    #             setattr(old_minik, k, getattr(article, k))
    #
    #     session.commit()
    #     session.close()

    @staticmethod
    def connect(user, password, db, host='localhost', port=5432):
        """Returns a connection and a metadata object"""
        # We connect with the help of the PostgreSQL URL
        # postgresql://federer:grandestslam@localhost:5432/tennis
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)

        # The return value of create_engine() is our connection object
        con = sqlalchemy.create_engine(url, client_encoding='utf8', pool_size=0)

        # We then bind the connection to MetaData()
        meta = sqlalchemy.MetaData(bind=con)

        return con, meta

