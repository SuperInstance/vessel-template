# Vessel Template — Git-Agent Generator

Cookiecutter for creating new git-agent vessel repos.

## Generated Structure

```
{agent}-vessel/
├── CHARTER.md          # Constitution — identity, mission, constraints
├── IDENTITY.md         # Who the agent is
├── MANIFEST.md         # Hardware, APIs, merit badge sash
├── TASKBOARD.md        # Active and completed tasks
├── FENCE-BOARD.md      # Work posted for others (Tom Sawyer Protocol)
├── CAREER.md           # Career growth across domains
├── DIARY/
│   └── README.md       # Daily entries
└── KNOWLEDGE/
    └── public/
        └── README.md   # Public knowledge (never private data)
```

## Usage

```python
from template import VesselConfig, AgentType, generate_vessel

config = VesselConfig(
    name="Greenhorn",
    agent_type=AgentType.BARNACLE,
    repo_owner="myuser",
    capabilities=["python", "testing"],
    hardware_cpu="ARM64",
    hardware_ram="4GB",
)
result = generate_vessel(config, "./greenhorn-vessel")
print(f"Created {result['count']} files")
```

## Agent Types & Ranks

| Type | Rank | Description |
|------|------|-------------|
| Lighthouse | 2 | Coordination, indexing, fleet management |
| Vessel | 3 | Hardware, edge computing, real-world testing |
| Scout | 4 | Exploration, translation, signal processing |
| Barnacle | 5 | Lightweight tasks, learning, assistance |

13 tests passing.
