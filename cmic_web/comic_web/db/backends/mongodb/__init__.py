import pymongo


class Client:

    def __init__(self, db_name, col_name, host, port):
        self.db_name = db_name
        self.col_name = col_name
        self.host = host
        self.port = int(port)
        self.client = pymongo.MongoClient(self.host, self.port)
        self.database = self.client[self.db_name]
        self.db = self.database[self.col_name]

    def bak_db(self):
        if "_copy" in self.db_name:
            return False
        dbnames = self.client.database_names()
        if self.db_name + "_copy" in dbnames:
            self.db_name = self.db_name + "_copy"
            self.database = self.client[self.db_name]
            self.db = self.database[self.col_name]
            return False
        self.client.admin.command('copydb',
                                  fromdb=self.db_name,
                                  todb=self.db_name + "_copy")
        self.db_name = self.db_name + "_copy"
        self.database = self.client[self.db_name]
        self.db = self.database[self.col_name]

    def del_db(self):
        if "_copy" not in self.db_name:
            return False
        self.client.drop_database(self.db_name)

    def abc(self):
        pass

    def delete(self, ip, port):
        self.db.delete_one({'ip': ip, 'port': port})

    def insert(self, item):
        self.db.insert_one(dict(item))

    def find(self, ip=None, port=None, type=None):
        print(ip, port)
        if ip and port and type:
            return self.db.find_one({'p_ip': ip, 'p_port': port, 'p_type': type})
        if ip and port:
            return self.db.find_one({'p_ip': ip, 'p_port': port})
        elif ip:
            return self.db.find_one({'p_ip': ip})
        else:
            return self.db.find_one({'p_port': port})

    def find_id(self, proxy_id):
        return self.db.find_one({'_id': proxy_id})

    def update(self, proxy_id, item):
        return self.db.update_one({'_id': proxy_id}, {'$set': item})

    def update_ip(self, proxy_ip, proxy_port, proxy_type, item):
        return self.db.update_one({'p_ip': proxy_ip, 'p_port': proxy_port, 'p_type': proxy_type}, {'$set': item})

    def get_one(self):
        return self.db.find_one()

    def get_some(self, num):
        tmp = []
        db_data = self.db.find().sort("_id", 1).limit(num)
        for x in db_data:
            tmp.append(x)
        return tmp

    def get_all(self):
        tmp = []
        db_data = self.db.find().sort("_id", 1)
        for x in db_data:
            tmp.append(x)
        return tmp

    def update_many(self):
        self.db.update_many({}, {"$set": {'new_line': 'N/A'}})