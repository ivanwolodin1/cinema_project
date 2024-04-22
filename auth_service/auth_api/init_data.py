from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import config
from models.base import Base
from models.role import Role

DATABASE_URL = (
    f'postgresql://'
    f'{config.POSTGRES_USERNAME}:{config.POSTGRES_PASSWORD}'
    f'@{config.POSTGRES_HOST}/{config.POSTGRES_DB_NAME}'
)


def init_data():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    roles = [Role(name='Admin'), Role(name='User')]
    session.add_all(roles)
    session.commit()

    session.close()


if __name__ == '__main__':
    init_data()
