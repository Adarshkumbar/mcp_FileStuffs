import json
from typing import Optional, List, Any
from mcp.types import CallToolResult, TextContent
from mcp_client import MCPClient


class ToolManager:
    @classmethod
    async def get_all_tools(
        cls, clients: dict[str, MCPClient]
    ) -> list[dict[str, Any]]:
        """Gets all tools from the provided clients."""
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    },
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    @classmethod
    async def execute_tool_requests(
        cls,
        clients: dict[str, MCPClient],
        tool_calls: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Executes OpenAI-style tool calls and returns 'tool' role messages."""
        tool_messages: list[dict[str, Any]] = []
        for tool_call in tool_calls:
            tool_call_id = tool_call.get("id", "")
            fn = (tool_call.get("function") or {}) if isinstance(tool_call, dict) else {}
            tool_name = fn.get("name", "")
            raw_args = fn.get("arguments", "{}")

            try:
                tool_input = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
            except Exception:
                tool_input = {}

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps({"error": f"Could not find tool '{tool_name}'"}),
                    }
                )
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = tool_output.content if tool_output else []
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                payload: dict[str, Any] = {"ok": not (tool_output and tool_output.isError), "content": content_list}
                tool_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(payload),
                    }
                )
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                print(error_message)
                tool_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps({"error": error_message}),
                    }
                )

        return tool_messages
