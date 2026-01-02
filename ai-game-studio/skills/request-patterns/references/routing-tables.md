# Request Routing Tables

Detailed routing tables for request classification.

## Quality Improvement Routing

| Domain | Analyzer | Implementer |
|--------|----------|-------------|
| Visual (textures/meshes) | quality-analyzer | asset-generator |
| Audio | sound-director | sfx-architect / music-architect |
| Code | tech-director | feature-implementer |
| Gameplay | design-reviewer | feature-implementer |

## Bug Fix Routing

| Symptom | Domain | Route To |
|---------|--------|----------|
| "Falls through", "clips", "collision" | Physics | feature-implementer |
| "Doesn't appear", "invisible" | Rendering | completion-auditor → feature-implementer |
| "Sound doesn't play" | Audio | integration-assistant |
| "Crashes", "panic", "error" | Code | tech-director → feature-implementer |
| "Desyncs", "rollback issues" | Netcode | rollback-reviewer → desync-investigator |
| "Slow", "lag", "stutters" | Performance | build-analyzer → optimizer |

## Feature Routing

| Feature Type | Primary Agent | Supporting Agents |
|--------------|---------------|-------------------|
| Game mechanic | feature-implementer | - |
| Visual feature | feature-implementer | asset-generator, integration-assistant |
| Audio feature | feature-implementer | sfx-architect, integration-assistant |
| UI element | feature-implementer | - |
| Complete system | feature-implementer | Multiple as needed |

## Asset Routing

| Asset Type | Design Agent | Generation Agent |
|------------|--------------|------------------|
| Texture | asset-designer | asset-generator |
| Mesh | asset-designer | asset-generator |
| Character | asset-designer | character-generator |
| Sound effect | sonic-designer | sfx-architect |
| Music | sonic-designer | music-architect |

**Always follow asset generation with:** integration-assistant

## Review Routing

| Review Type | Agent |
|-------------|-------|
| Code quality | tech-director |
| Visual coherence | art-director |
| Audio coherence | sound-director |
| Overall vision | creative-director |
| GDD alignment | gdd-implementation-tracker |
| Release readiness | release-validator |
| Netcode safety | rollback-reviewer |

## Multi-Domain Example

**Request:** "Add a power-up system with visual effects and sounds"

```
Domains: Gameplay + Visual + Audio

Tasks:
1. [Parallel] Design power-up mechanics (mechanic-designer)
2. [Parallel] Design power-up visuals (asset-designer)
3. [Parallel] Design power-up sounds (sonic-designer)
4. [After 2] Generate visual assets (asset-generator)
5. [After 3] Generate audio assets (sfx-architect)
6. [After 1,4,5] Implement system (feature-implementer)
7. [After 6] Integrate assets (integration-assistant)
8. [After 7] Verify completion (completion-auditor)
```
