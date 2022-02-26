import asyncio
import json

class JSONClient:
    def __init__(self, address="127.0.0.1", port=8888):
        self.address = address
        self.port = port

    def send(self, output, verbose=False):
        # dump to JSON
        payload = json.dumps(output)
        if verbose:
            print(f'Send: {payload!r}')

        asyncio.run(self.async_write(payload))

    async def async_write(self, message):
        # send payload over socket
        reader, writer = await asyncio.open_connection(self.address, self.port)
        writer.write(message.encode())
        writer.close()

if __name__ == "__main__":
    test_data = {"detection": {"labels": [0], "boxes": [[0,0,1,1]], "scores": [0.5]}}
    client = JSONClient()
    client.send(test_data, verbose=1)