import time

from es_index import create_es_index
from etl import ETL

if __name__ == '__main__':
    create_es_index()
    etl_obj = ETL()

    while True:
        etl_obj.run()
        time.sleep(1)
