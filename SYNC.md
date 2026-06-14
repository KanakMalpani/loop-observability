# Sync policy

| Artifact | Canonical home | This repo |
|----------|----------------|-----------|
| LSS / LES specs | [Loop Core Engineering](https://github.com/KanakMalpani/Loop-Core-Engineering) | Pins only in LTF |
| LTF schema | **This repo** `specs/ltf-0.1.schema.json` | Bundled copy in `loopotel/schemas/` |
| LoopNet trajectory | [loopnet](https://github.com/KanakMalpani/loopnet) | Export via `trajectory_from_trace()` |
| LoopGym runtime | [LoopGym](https://github.com/KanakMalpani/LoopGym) | Integration in `loopotel.integrations.loopgym` |

Do not fork LSS/LES schemas here. Reference pins in every LTF document via `spec_pins`.
