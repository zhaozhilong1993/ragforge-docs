---
sidebar_position: 4
slug: /mcp_server
---

# RAGForge MCP server overview

The RAGForge Model Context Protocol (MCP) server operates as an independent component that complements the RAGForge server. However, it requires a RAGForge server to work functionally well, meaning, the MCP client and server communicate with each other in MCP HTTP+SSE mode (once the connection is established, server pushes messages to client only), and responses are expected from RAGForge server.

The MCP server currently offers a specific tool to assist users in searching for relevant information powered by RAGForge DeepDoc technology:

- **retrieve**: Fetches relevant chunks from specified `dataset_ids` and optional `document_ids` using the RAGForge retrieve interface, based on a given question. Details of all available datasets, namely, `id` and `description`, are provided within the tool description for each individual dataset.

## Launching the MCP Server

Similar to launching the RAGForge server, the MCP server can be started either from source code or via Docker.

### Launch Modes

The MCP server supports two launch modes:

1. **Self-Host Mode**:

   - In this mode, the MCP server is launched to access a specific tenant's datasets.
   - This is the default mode.
   - The `--api_key` argument is **required** to authenticate the server with the RAGForge server.
   - Example:
     ```bash
     uv run mcp/server/server.py --host=127.0.0.1 --port=9382 --base_url=http://127.0.0.1:9380 --mode=self-host --api_key=ragforge-xxxxx
     ```

1. **Host Mode**:

   - In this mode, the MCP server allows each user to access their own datasets.
   - To ensure secure access, a valid API key must be included in the request headers to identify the user.
   - The `--api_key` argument is **not required** during server launch but must be provided in the headers on each client request for user authentication.
   - Example:
     ```bash
     uv run mcp/server/server.py --host=127.0.0.1 --port=9382 --base_url=http://127.0.0.1:9380 --mode=host
     ```

### Launching from Source Code

All you need to do is stand on the right place and strike out command, assuming you are on the project working directory.

```bash
uv run mcp/server/server.py --host=127.0.0.1 --port=9382 --base_url=http://127.0.0.1:9380 --api_key=ragforge-xxxxx
```

For testing purposes, there is an [MCP client example](#example_mcp_client) provided, free to take!

#### Required Arguments

- **`host`**: Specifies the server's host address.
- **`port`**: Defines the server's listening port.
- **`base_url`**: The address of the RAGForge server that is already running and ready to handle tasks.
- **`mode`**: Launch mode, only accept `self-host` or `host`.
- **`api_key`**: Required when `mode` is `self-host` to authenticate the MCP server with the RAGForge server.

Here are three augments required, the first two,`host` and `port`, are self-explained. The`base_url` is the address of the ready-to-serve RAGForge server to actually perform the task.

### Launching from Docker

Building a standalone MCP server image is straightforward and easy, so we just proposed a way to launch it with RAGForge server here.

#### Alongside RAGForge

As MCP server is an extra and optional component of RAGForge server, we consume that not everybody going to use it. Thus, it is disable by default.
To enable it, simply find `docker/docker-compose.yml` to uncomment `services.ragforge.command` section.

```yaml
services:
  ragforge:
    ...
    image: ${RAGFORGE_IMAGE}
    # example to setup MCP server
    command:
      - --enable-mcpserver
      - --mcp-host=0.0.0.0
      - --mcp-port=9382
      - --mcp-base-url=http://127.0.0.1:9380
      - --mcp-script-path=/ragforge/mcp/server/server.py
      - --mcp-mode=self-host # `self-host` or `host`
      - --mcp--host-api-key="ragforge-xxxxxxx" # only need to privide when mode is `self-host`
```

Then launch it normally `docker compose -f docker-compose.yml`.

```bash
ragforge-server  | Starting MCP Server on 0.0.0.0:9382 with base URL http://127.0.0.1:9380...
ragforge-server  | Starting 1 task executor(s) on host 'dd0b5e07e76f'...
ragforge-server  | 2025-04-18 15:41:18,816 INFO     27 ragforge_server log path: /ragforge/logs/ragforge_server.log, log levels: {'peewee': 'WARNING', 'pdfminer': 'WARNING', 'root': 'INFO'}
ragforge-server  | 
ragforge-server  | __  __  ____ ____       ____  _____ ______     _______ ____
ragforge-server  | |  \/  |/ ___|  _ \     / ___|| ____|  _ \ \   / / ____|  _ \
ragforge-server  | | |\/| | |   | |_) |    \___ \|  _| | |_) \ \ / /|  _| | |_) |
ragforge-server  | | |  | | |___|  __/      ___) | |___|  _ < \ V / | |___|  _ <
ragforge-server  | |_|  |_|\____|_|        |____/|_____|_| \_\ \_/  |_____|_| \_\
ragforge-server  |     
ragforge-server  | MCP launch mode: self-host
ragforge-server  | MCP host: 0.0.0.0
ragforge-server  | MCP port: 9382
ragforge-server  | MCP base_url: http://127.0.0.1:9380
ragforge-server  | INFO:     Started server process [26]
ragforge-server  | INFO:     Waiting for application startup.
ragforge-server  | INFO:     Application startup complete.
ragforge-server  | INFO:     Uvicorn running on http://0.0.0.0:9382 (Press CTRL+C to quit)
ragforge-server  | 2025-04-18 15:41:20,469 INFO     27 found 0 gpus
ragforge-server  | 2025-04-18 15:41:23,263 INFO     27 init database on cluster mode successfully
ragforge-server  | 2025-04-18 15:41:25,318 INFO     27 load_model /ragforge/rag/res/deepdoc/det.onnx uses CPU
ragforge-server  | 2025-04-18 15:41:25,367 INFO     27 load_model /ragforge/rag/res/deepdoc/rec.onnx uses CPU
ragforge-server  |         ____   ___    ______ ______ __               
ragforge-server  |        / __ \ /   |  / ____// ____// /____  _      __
ragforge-server  |       / /_/ // /| | / / __ / /_   / // __ \| | /| / /
ragforge-server  |      / _, _// ___ |/ /_/ // __/  / // /_/ /| |/ |/ / 
ragforge-server  |     /_/ |_|/_/  |_|\____//_/    /_/ \____/ |__/|__/                             
ragforge-server  | 
ragforge-server  |     
ragforge-server  | 2025-04-18 15:41:29,088 INFO     27 RAGForge version: v0.18.0-285-gb2c299fa full
ragforge-server  | 2025-04-18 15:41:29,088 INFO     27 project base: /ragforge
ragforge-server  | 2025-04-18 15:41:29,088 INFO     27 Current configs, from /ragforge/conf/service_conf.yaml:
ragforge-server  |  ragforge: {'host': '0.0.0.0', 'http_port': 9380}
...
ragforge-server  |  * Running on all addresses (0.0.0.0)
ragforge-server  |  * Running on http://127.0.0.1:9380
ragforge-server  |  * Running on http://172.19.0.6:9380
ragforge-server  |   ______           __      ______                     __            
ragforge-server  |  /_  __/___ ______/ /__   / ____/  _____  _______  __/ /_____  _____
ragforge-server  |   / / / __ `/ ___/ //_/  / __/ | |/_/ _ \/ ___/ / / / __/ __ \/ ___/
ragforge-server  |  / / / /_/ (__  ) ,<    / /____>  </  __/ /__/ /_/ / /_/ /_/ / /    
ragforge-server  | /_/  \__,_/____/_/|_|  /_____/_/|_|\___/\___/\__,_/\__/\____/_/                               
ragforge-server  |     
ragforge-server  | 2025-04-18 15:41:34,501 INFO     32 TaskExecutor: RAGForge version: v0.18.0-285-gb2c299fa full
ragforge-server  | 2025-04-18 15:41:34,501 INFO     32 Use Elasticsearch http://es01:9200 as the doc engine.
...
```

You are ready to brew🍺!

## Testing and Usage

Typically, there are various ways to utilize an MCP server. You can integrate it with LLMs or use it as a standalone tool. You find the way.

### Example MCP Client {#example_mcp_client}

```python
#
#  Copyright 2025 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#


from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


async def main():
    try:
        # To access RAGForge server in `host` mode, you need to attach `api_key` for each request to indicate identification.
        # async with sse_client("http://localhost:9382/sse", headers={"api_key": "ragforge-IyMGI1ZDhjMTA2ZTExZjBiYTMyMGQ4Zm"}) as streams:
        async with sse_client("http://localhost:9382/sse") as streams:
            async with ClientSession(
                streams[0],
                streams[1],
            ) as session:
                await session.initialize()
                tools = await session.list_tools()
                print(f"{tools.tools=}")
                response = await session.call_tool(name="ragforge_retrieval", arguments={"dataset_ids": ["ce3bb17cf27a11efa69751e139332ced"], "document_ids": [], "question": "How to install neovim?"})
                print(f"Tool response: {response.model_dump()}")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    from anyio import run

    run(main)
```

## Security and Concerns

Since MCP technology is still in booming age and there are still no official Authentication and Authorization best practices to follow, RAGForge uses `api_key` to validate the identification, and it is required to perform any operations mentioned in the preview section. Obviously, this is not a premium solution to do so, thus this RAGForge MCP server is not expected to exposed to public use as it could be highly venerable to be attacked. For local SSE server, bind only to localhost (127.0.0.1) instead of all interfaces (0.0.0.0). For additional guidance, you can refer to [MCP official website](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).
