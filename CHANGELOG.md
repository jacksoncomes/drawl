# Changelog

All notable changes to this specification are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [semver](https://semver.org), as scoped in `README.md` § 8.

## [2.0.0] — 2026-09-15

Major. The containment model changed shape, and the project changed from a personal
configuration into something a stranger can install.

### Added
- **The hard filter** (`SKILL.md` § 0). A single binary gate — *is this text a chat
  message spoken to the user?* — applied to every piece of text produced. Replaces the
  three-zone model as the primary control. The zones survive as the description of what
  happens inside the "yes" branch.
- **Voice packs** (`voices/`). The gate is register-agnostic, so the same containment
  engine now carries `noir` (debugging), `documentary` (legacy code) and `sommelier`
  (code review) alongside the default. Each pack names the engineering task it suits.
- **`scripts/check-egress.py`** and a pre-commit hook enforcing the gate mechanically.
  Six detector classes. A specification that relies on an agent remembering a rule has
  one point of failure; this is the second.
- **`scripts/count-lexicon.py --check`**, because the coverage table states a number and
  a specification that takes itself seriously does not ship unverified claims.
- The collusive "us" — *cowfolk like us*, *us cowpokes*, *folks like you an' me* — as a
  first-class bucket. The warmest move the register has, and it was entirely absent.
- Two buckets built for technical work: **machine states** (`hangin' fire`, `full as a
  tick`, `ornery`) and **it won't work / refuted** (`that dog won't hunt`, `nailed to
  the counter`). Dialect applied to hardware is the highest-yield collision available.
- Construction templates expanded to seven, including the collusive-us frame and
  the dialect-times-technical-noun collision that drives most of the humour.
- RT-008: a reply containing only common slang is now a test failure.

### Changed
- **Dropped g's are now the default in conversational text, not a seasoning.** Version
  1.0 said "sparingly" and "do not phonetically respell every word", which produced a
  narrator rather than a speaker. The line that replaces it is principled: dropped g's
  and elisions render how the dialect sounds; respelling neutral words (`wuz`, `sez`,
  `thet`) is eye-dialect, which signals the speaker is uneducated rather than that they
  have an accent. The first is voice; the second is mockery.
- **The uncommon-entry rule inverted from a ceiling to a floor.** Version 1.0 tagged 71
  entries rare and rationed them to one per reply. They then never appeared. Rationing
  something already marked rare guarantees it is never spent.
- Flourish budget raised from ≤2 to 2–3.
- Lexicon grown from 102 entries to **162**, of which 71 are uncommon.
- README rewritten to lead with the containment guarantee rather than the cowboy. The
  novel thing here is not the voice; it is that the voice cannot reach your repository.
- The address term is documented as configurable. It is one word in one place.

### Fixed
- Coverage table was off by one against the file it described.

---

## [1.0.0] — 2026-09-15

First public release. Supersedes an unversioned internal rule.

### Added
- Three-zone positional model (`SKILL.md` § 2). Flavour is permitted by sentence
  position rather than by topic, which is what makes the constraint enforceable.
- Flourish budget with an explicit ceiling, floor, and token-neutrality requirement
  (`README.md` § 4).
- Hard prohibitions on bad news and on any artefact persisting to disk
  (`SKILL.md` § 4, `README.md` § 6), with severity levels.
- `reference/lexicon.md` — 102 entries indexed by intent, tagged for register.
- Seven conformance test cases (`README.md` § 7).
- Six worked examples, three of them deliberately non-conforming (`SKILL.md` § 6).
- Construction templates, so that phrasing can be generated rather than recalled.

### Changed
- **Frequency raised.** The predecessor rule specified "roughly one flourish per few
  messages". In deployment this produced an agent that appeared to have forgotten the
  instruction entirely. The new floor treats two consecutive flourish-free replies as a
  defect rather than as restraint.
- **Register narrowed.** The predecessor specified generic cowboy slang. This release
  targets one voice specifically, which is both funnier and easier to check against.
- Prohibited-context list expanded from four items to eighteen, and given a governing
  principle — *if it outlives the chat window, it's plain* — so the list does not need
  to be exhaustive to be correct.

### Removed
- `sweetheart` as a form of address. It belongs to the source character's condescension
  register and is aimed at people he is about to inconvenience.
- `pardner`. Theme park.

---

[2.0.0]: https://github.com/jacksoncomes/drawl/releases/tag/v2.0.0
[1.0.0]: https://github.com/jacksoncomes/drawl/releases/tag/v1.0.0
