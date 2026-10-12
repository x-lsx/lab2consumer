import argparse
import asyncio
import configparser
import os

import queue_transport
import socket_transport
from pg_loader import PostgreSQLLoader


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["socket", "queue"], required=True)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

    db = config["database"]
    db_config = {
        "dbname": db["dbname"],
        "user": db["user"],
        "password": db["password"],
        "host": db["host"],
        "port": db["port"],
    }
    loader = PostgreSQLLoader(db_config)

    if args.transport == "socket":
        await socket_transport.serve(
            config.get("socket", "host", fallback="0.0.0.0"),
            config.getint("socket", "port", fallback=9000),
            loader,
            config.get("socket", "cert"),
            config.get("socket", "key"),
        )
    else:
        await queue_transport.consume(loader)


if __name__ == "__main__":
    asyncio.run(main())