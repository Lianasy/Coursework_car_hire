import redis
import mysql.connector
import couchdb

class Connection:
    def __init__(self, redis_host, mysql_host, mysql_user, mysql_password, mysql_db, couch_user, couch_password, couch_host):
        try:
            self.redis_connection = redis.Redis(redis_host, decode_responses=True)
            self.mysql_connection = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db)
            self.couchdb_connection = couchdb.Server(f"http://{couch_user}:{couch_password}@{couch_host}:5984/")
        except Exception as e:
            print("Fail", e)


connection = Connection("***.***.***.***",
                        "***.***.***.***", "****", "*******", "******",
                        "******", "*******", "***.***.***.***")
