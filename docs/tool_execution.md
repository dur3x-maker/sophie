# Tool Execution

- Tool implementations return `ToolResult` only.
- Worker code does not execute tools directly.
- `ToolManager` resolves a tool through `ToolRegistry`.
- `ToolExecutor` is the only layer that calls `BaseTool.execute`.
- Tool failures are returned as failed `ToolResult` values.
