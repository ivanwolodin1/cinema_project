from dataclasses import asdict

from db_connections import open_postgres_connection
from logger import logger


class PostgresSaver:
    def __init__(self):
        ...

    def save_data(self, data_chunk: dict) -> None:
        try:
            logger.info(
                'Inserting chunk into: {0}'.format(data_chunk['postgres_table']),
            )
            with open_postgres_connection() as pg_cursor:
                args = ','.join(
                    pg_cursor.mogrify(
                        data_chunk['string_pattern'],
                        tuple([asdict(item_chunk)[chunk] for chunk in data_chunk['ordered_keys']]),
                    ).decode()
                    for item_chunk in data_chunk['res']
                )
                pg_cursor.execute(data_chunk['postgres_sql_upsert'].format(args))
        except Exception as error:
            logger.info('Cannot upsert data: Error: {0}'.format(error))
