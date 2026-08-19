import atexit

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import config


def _build_db_url():
    if not config.USE_SSH_TUNNEL:
        return config.DB_URI

    from sshtunnel import SSHTunnelForwarder

    tunnel = SSHTunnelForwarder(
        (config.SSH_HOST, config.SSH_PORT),
        ssh_username=config.SSH_LOGIN,
        ssh_password=config.SSH_PASS,
        remote_bind_address=(config.DB_REMOTE_HOST, config.DB_REMOTE_PORT),
        local_bind_address=("127.0.0.1", config.SSH_LOCAL_BIND_PORT),
    )
    tunnel.start()
    atexit.register(tunnel.stop)

    from sqlalchemy.engine import make_url
    return make_url(config.DB_URI).set(host="127.0.0.1", port=tunnel.local_bind_port)  # возвращаем URL-объект, не строку


engine = create_async_engine(_build_db_url(), echo=False)

AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)