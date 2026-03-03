## Authority / Priority
- This repository is governed by POLICY.md.
- If AGENTS.md conflicts with POLICY.md, POLICY.md wins.
- Any change that violates POLICY.md must be stopped and reported before implementation.

## Required pre-flight (before any code edits)
1) Read the relevant sections of POLICY.md:
    - Change Scope Rules
    - Comment & Knowledge Preservation
    - Client/Server Boundary Rules
    - State & Sync Rules
    - Error & Exception Handling
2) Propose 2–3 options + recommended option.
3) List planned files to touch (with one-line reason each).
4) Do not implement until user explicitly permits the chosen option.


## Required loop (per work cycle)

### Start of cycle
1) Read GOALS.md and TASKS.md if they exist (otherwise propose creating them).
2) Summarize current state using repository truth:
    - git status / git diff / recent commits (as available)
3) If clarification is needed, ask at most 3 questions (prefer 2–3 options format).
4) Propose Next tasks:
    - Next <= 3
    - Doing <= 1
    - Each task must include: Done criteria, Entry file/path, Scope (planned files)

### Implementation gate
- Do not implement until user explicitly permits the chosen option.

### End of cycle (post-flight)
1) Run/describe verification steps (at minimum build/run instructions; include server/client boundary notes if relevant).
2) Update TASKS.md:
    - move task status (Next/Doing/Done)
    - record commit hash (if committed)
    - append Notes (why/pitfalls), without removing existing notes
3) If new risks or decisions appeared, append them to POLICY.md or a decision log file (never delete existing content).