# Server stores no code — pure relay only

The server receives a submission and immediately broadcasts it to all connected clients, then discards it. No code is held in server memory between broadcasts. The only server-side state is the set of open WebSocket connections.

This was a deliberate choice over an in-memory cache (which would let late joiners catch up). We rejected caching because it creates a session-boundary problem on a continuously-running hosted server (fly.io): without authentication, there is no safe way to clear stale submissions between classes. Keeping the server stateless eliminates that problem entirely — each client's browser memory is their own session.

## Consequences

Late joiners see no submissions made before they connected. This is acceptable in a classroom setting where the teacher opens the app before telling students to submit.
