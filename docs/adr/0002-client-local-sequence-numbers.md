# Submissions are numbered locally per client, not globally by the server

Each client assigns its own sequential number to submissions in the order they arrive. Two clients connected at different times will assign different numbers to the same submission.

A server-assigned global counter was considered, but rejected because it would require the server to maintain numeric state — violating the pure-relay constraint in ADR-0001. Since the Show tab selection is local-only and submissions are identified by display name rather than number, consistent cross-client numbering has no practical value.
