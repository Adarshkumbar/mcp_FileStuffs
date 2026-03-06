from mcp_client import MCPClient
from core.tools import ToolManager
import json
from core.ollama import Ollama


class Chat:
    def __init__(self, llm_service: Ollama, clients: dict[str, MCPClient]):
        self.llm_service: Ollama = llm_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[dict] = []
        self._initialized = False

    def _ensure_system_message(self):
        if self._initialized:
            return
        self._initialized = True
        self.messages.insert(
            0,
            {
                "role": "system",
                "content": (
                    "You can call tools when needed. If a tool is required, use tool calling "
                    "(function/tool_calls) rather than printing JSON. After you receive tool output, "
                    "use it to answer the user."
                ),
            },
        )

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        self._ensure_system_message()
        await self._process_query(query)

        while True:
            tool_specs = await ToolManager.get_all_tools(self.clients)
            tool_names = {
                (t.get("function") or {}).get("name")
                for t in tool_specs
                if isinstance(t, dict)
            }

            result = self.llm_service.chat(
                messages=self.messages,
                tools=tool_specs,
            )
            assistant_message = result.message
            self.messages.append(assistant_message)

            tool_calls = assistant_message.get("tool_calls") or []
            if tool_calls:
                tool_messages = await ToolManager.execute_tool_requests(
                    self.clients, tool_calls
                )
                self.messages += tool_messages
                continue

            # Fallback: some local models may output a JSON "call" instead of emitting tool_calls.
            content = assistant_message.get("content")
            if isinstance(content, str):
                try:
                    maybe_call = json.loads(content)
                except Exception:
                    maybe_call = None

                if (
                    isinstance(maybe_call, dict)
                    and isinstance(maybe_call.get("name"), str)
                    and maybe_call.get("name") in tool_names
                    and isinstance(maybe_call.get("arguments"), dict)
                ):
                    pseudo_call = [
                        {
                            "id": "fallback_tool_call_1",
                            "type": "function",
                            "function": {
                                "name": maybe_call["name"],
                                "arguments": json.dumps(maybe_call["arguments"]),
                            },
                        }
                    ]
                    tool_messages = await ToolManager.execute_tool_requests(
                        self.clients, pseudo_call
                    )
                    self.messages += tool_messages
                    continue

            final_text_response = assistant_message.get("content") or ""
            break

        return final_text_response
