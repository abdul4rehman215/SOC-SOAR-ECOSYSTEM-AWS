# V2 Phase 5 RAG + Memory Poisoning Lab

Simulates a local RAG and memory path:

```text
retrieval query -> retrieved context -> source trust decision -> memory write decision -> /var/log/ai-demo/rag-memory-events.jsonl -> Wazuh 100401-100405 -> Flow C2
```

No external web requests, no vector DB, no production memory, and no real tool execution.
