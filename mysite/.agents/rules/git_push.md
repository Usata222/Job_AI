# Git Push Trigger Rule

Whenever the user says or types **"push"** (or variations like "push to github", "push code"):
1. Immediately stage appropriate modified/untracked files (`git add .` or specific changed files, ensuring sensitive files like `.env` remain ignored).
2. Commit with a clear, concise message describing what changed.
3. Push directly to `origin <current-branch>`.
4. Respond with a single concise line confirming the push (e.g., `Pushed <hash> to origin/<branch>: <message>`) without unnecessary questions or commentary.

