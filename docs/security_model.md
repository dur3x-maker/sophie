# Security Model

Security is a separate layer because LLM output is not trusted application logic.

The agent loop can decide that a tool should be called, but the decision is only a
request. The application owns execution.

The mandatory path is:

```text
AgentLoop -> ToolManager -> ToolExecutor -> Tool
```

`ToolExecutor` is the single point where command-like inputs are validated before tool
code can run. This keeps future SSH, Docker, Git, Shell, Filesystem, and HTTP tools from
duplicating security rules or inventing incompatible checks.

`SecurityPolicy` owns the rules. `SecurityValidator` applies those rules. This keeps
blocked patterns and risk-level settings out of individual tools and makes the policy
replaceable without rewriting workers.

Future `CONFIRMATION_REQUIRED` behavior should be added in this layer by returning or
raising a confirmation decision before execution, not by letting tools prompt users
directly.
