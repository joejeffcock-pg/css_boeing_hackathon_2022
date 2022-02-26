import asyncio
import json

class JSONClient:
    def __init__(self, address="127.0.0.1", port=8888):
        self.address = address
        self.port = port

    async def send(self, output, verbose=False):
        # dump to JSON and send payload over socket
        reader, writer = await asyncio.open_connection(self.address, self.port)
        message = json.dumps(output)

        if verbose:
            print(f'Send: {message!r}')
        writer.write(message.encode())
        writer.close()

if __name__ == "__main__":
    test_data = {"detection": {"labels": [0], "boxes": [[0,0,1,1]], "scores": [0.5]}}
    client = JSONClient()
    asyncio.run(client.send(test_data, verbose=1))