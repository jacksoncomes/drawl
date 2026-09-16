# Voice packs

The containment model in `SKILL.md` — the hard filter (§0), the zones (§2), the dial
(§1), the prohibitions (§4) — is **register-agnostic**. It constrains *where* voice is
allowed, not *which* voice.

A voice pack replaces §3 (how the voice sounds) and the lexicon. Everything else in
`SKILL.md` applies unchanged, including every prohibition. A pack that relaxes §0 is
not a voice pack; it is a bug.

## Using one

Point the skill at a pack by replacing the "how it sounds" section and the lexicon
reference. The simplest approach is to copy the pack's body into `SKILL.md` § 3 and
point `reference/lexicon.md` at the pack's own lexicon.

Every pack ships with: an identity, address terms, a cadence spec, a compact lexicon
indexed by intent, and one worked example demonstrating the technical parts staying
plain.

## The packs

| Pack | Register | Best at |
|---|---|---|
| **cowboy** (default, in `SKILL.md`) | Laconic Western; The Ghoul, *Fallout* | General work; handing over results |
| [`noir.md`](noir.md) | Hardboiled detective | **Debugging.** A stack trace is a witness statement |
| [`documentary.md`](documentary.md) | Hushed nature-documentary narration | **Reading unfamiliar or legacy code.** Observing wildlife that has not been disturbed in years |
| [`sommelier.md`](sommelier.md) | Wine tasting notes | **Code review.** Structured contempt, delivered as appreciation |

The pairing is the point. Each register happens to be *good at* a real engineering
activity, because each evolved to describe a situation that activity resembles. A
detective's job and a debugger's job are the same job.

## Writing a pack

A pack is accepted if it:

1. **Obeys § 0 without modification.** The hard filter is the whole product. A funny
   voice with no containment is a prompt, not a skill.
2. **Names the task it suits.** "It's funny" is not a use case. The packs that get used
   are the ones that make a specific job better.
3. **Indexes its lexicon by intent**, not alphabetically — *it worked*, *it's broken*,
   *it's suspicious*, *I was wrong*. An alphabetical wordlist is a wordlist nobody opens.
4. **Draws on an attested register.** A documented dialect, a named genre, or a
   specific published body of work. Invented whimsy goes stale in a week.
5. **Ships one worked example** where the technical content stays plain while the
   conversational frame carries voice. This is the example contributors most often
   omit and the one readers most need.
6. **Impersonates no real, living individual.** Register and genre, not a named
   person's voice.

Packs that would be welcome and do not exist yet: ship's log, dungeon master,
air-traffic control, court stenographer, medieval chronicler, sports commentary,
Victorian naturalist correspondence.
