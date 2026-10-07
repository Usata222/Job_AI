# Git Push Trigger Rule

Whenever the user says or types **"push"** (or variations like "push to github", "push code"):
1. Proactively inspect modified and untracked files (`git status`, `git diff`).
2. Ensure sensitive files (`.env`, database files, backups) remain excluded in `.gitignore`.
3. Stage all appropriate changes (`git add .`).
4. Generate a clear, descriptive commit message summarizing the changes.
5. Commit and push directly to `origin <current-branch>` (e.g. `git push origin main`).
6. Report a concise summary of the pushed commit and files to the user.
