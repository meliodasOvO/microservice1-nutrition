# service_factory.py
from framework.services.service_factory import BaseServiceFactory
import mysql.connector

# 数据库配置
config = {
    'user': 'root',
    'password': 'lisijun123',
    'host': 'localhost',
    'database': 'nutrition_db'
}

class ServiceFactory(BaseServiceFactory):
    @classmethod
    def get_connection(cls):
        # 提供数据库连接
        return mysql.connector.connect(**config)
