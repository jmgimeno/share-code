# Code Sharing

A real-time classroom tool for sharing code snippets between a teacher and students during a session.

## Language

**Submission**:
A piece of code sent by a client, carrying a language, an optional display name, and the code text itself. Once broadcast, the server retains no copy.
_Avoid_: snippet, message, post

**Display name**:
An optional author label attached to a submission. Stored in the browser's localStorage and reused across submissions. Shown alongside the local sequence number in the Show tab.
_Avoid_: username, author, identity

**Local sequence number**:
The per-client sequential index assigned to a submission in the order it was received. Two clients connected at different times will assign different numbers to the same submission.
_Avoid_: ID, global ID, submission ID

**Relay**:
The server's sole role: receive a submission from any connected client and forward it to all currently connected clients, including the sender. The server stores no code.
_Avoid_: broadcast server, message broker

**Submit tab**:
The UI view where a client composes and sends a submission.
_Avoid_: input view, send tab

**Show tab**:
The UI view where a client browses received submissions and selects one to display with syntax highlighting. Selection is local — it does not affect other clients.
_Avoid_: display tab, viewer, projector tab

**Room**:
A named, isolated group of connected clients whose submissions are not visible to clients outside the room. Not yet implemented; reserved for future parallel-session support.
_Avoid_: channel, session, group
