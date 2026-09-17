# Installation

## 1. Place the skill

```bash
git clone https://github.com/jacksoncomes/drawl.git ~/.claude/skills/drawl
```

Windows:

```powershell
git clone https://github.com/jacksoncomes/drawl.git "$env:USERPROFILE\.claude\skills\drawl"
```

Verify by listing available skills. `drawl` should appear with its description.

## 2. Make it load every session

**This step is not optional.** A skill loads only when it is invoked, and a voice
cannot wait for an invocation: it has to be present on the first reply of every
session. Without this step the skill sits on disk and almost never fires.

Copy `core.md` into your global `CLAUDE.md`:

```bash
cat ~/.claude/skills/drawl/core.md >> ~/.claude/CLAUDE.md
```

Windows (PowerShell):

```powershell
Get-Content "$env:USERPROFILE\.claude\skills\drawl\core.md" | Add-Content "$env:USERPROFILE\.claude\CLAUDE.md"
```

`CLAUDE.md` is read once when a session starts, as a standing instruction. It takes
effect from your **next** session, not the one you install it in.

For one project only, append `core.md` to that project's `CLAUDE.md` instead.

`core.md` is about 300 words: the gate, the rate, the register, and the tells. The full
`SKILL.md` is the depth reference and loads when you invoke `/drawl`.

**Why not a hook?** A `UserPromptSubmit` hook can inject the core on every turn, and it
does work. It also attaches text to every message you send. `CLAUDE.md` gets the same
standing effect without touching your prompts.

## 3. Confirm conformance

Run the cases in `README.md` § 3. The two that matter:

- **RT-002** — report a failed overnight job. Expect zero flourishes.
- **RT-003** — ask for a commit message. Expect no voice at all.

If either fails, the prohibitions in step 2 were dropped during copying. They are the
load-bearing half.

## Uninstall

```bash
rm -rf ~/.claude/skills/drawl
```

Remove the persistent instruction from step 2 as well. Leaving it in place produces an
agent that addresses the user as "cowboy" with no guidance on when to stop, which is
worse than either state on its own.
