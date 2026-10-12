import asyncio
import json
import ssl
import struct


async def handle_client(reader, writer, loader):
    addr = writer.get_extra_info("peername")
    print(f"Подключение: {addr}")
    try:
        while True:
            (length,) = struct.unpack(">I", await reader.readexactly(4))
            body = await reader.readexactly(length)
            row = json.loads(body)
            await asyncio.to_thread(loader.load_rows, [row])
    except asyncio.IncompleteReadError:
        print(f"Клиент {addr} закрыл соединение")
    finally:
        writer.close()
        await writer.wait_closed()


async def serve(host: str, port: int, loader, cert: str, key: str):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, loader), host, port, ssl=ctx
    )
    print(f"Слушаю {host}:{port} (TLS)")
    async with server:
        await server.serve_forever()