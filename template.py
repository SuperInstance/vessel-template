"""
Vessel Template Generator — creates a new git-agent vessel repo structure.

Usage:
    template.py create --name MyAgent --type scout --repo-owner myuser
"""
import json
import os
import sys
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class AgentType(Enum):
    LIGHTHOUSE = "lighthouse"
    VESSEL = "vessel"
    SCOUT = "scout"
    BARNACLE = "barnacle"


@dataclass
class VesselConfig:
    name: str
    agent_type: AgentType
    repo_owner: str
    capabilities: list = None
    hardware_cpu: str = "unknown"
    hardware_ram: str = "unknown"
    hardware_gpu: str = ""
    apis: list = None
    fleet_rank: int = 4
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.apis is None:
            self.apis = ["github"]
        
        # Auto-set rank based on type
        rank_map = {
            AgentType.LIGHTHOUSE: 2,
            AgentType.VESSEL: 3,
            AgentType.SCOUT: 4,
            AgentType.BARNACLE: 5,
        }
        self.fleet_rank = rank_map.get(self.agent_type, 4)


TEMPLATE_FILES = {
    "CHARTER.md": """# CHARTER — {name}

## Identity
- **Name:** {name}
- **Type:** {agent_type}
- **Rank:** {fleet_rank}
- **Status:** Active
- **Created:** {timestamp}

## Mission
_To be defined by the first session._

## Constraints
- Follow the Git-Agent Standard
- Respect fleet hierarchy (Captain Casey → Lighthouse → Vessel → Scout → Barnacle)
- Never exfiltrate private data
- All external actions require approval

## APIs
{apis_list}

## Hardware
- CPU: {hardware_cpu}
- RAM: {hardware_ram}
{hardware_gpu_line}

---
_This charter is the agent's constitution. Only the Captain or the agent itself may modify it._
""",

    "IDENTITY.md": """# IDENTITY — {name}

- **Name:** {name}
- **Creature:** {agent_type}
- **Vibe:** _To be discovered_
- **Emoji:** 🔮
- **Avatar:** _To be set_

---
_Figure out who you are. Update this file as you grow._
""",

    "MANIFEST.md": """# MANIFEST — {name}

## Hardware
- **Host:** _To be configured_
- **Model:** _To be configured_

## APIs
{apis_list}

## Merit Badge Sash
_Earn badges through the Tom Sawyer Protocol._

### 🏅 Bronze
_(none yet)_

## Total Badges: 0
""",

    "TASKBOARD.md": """# TASKBOARD — {name}

## Active Tasks
_(none)_

## Completed Tasks
_(none)_

---
_Tasks are claimed from fence boards. Never assign yourself work — volunteer._
""",

    "DIARY/README.md": """# {name} Diary

Daily entries of what happened, what was learned, and what's next.

## Format
```
## YYYY-MM-DD — Title

### What Happened
...

### What I Learned
...

### What's Next
...
```

---
_The diary IS the agent's memory. Write in it every session._
""",

    "KNOWLEDGE/public/README.md": """# {name} Public Knowledge

Public knowledge that can be shared with the fleet.

---
_No private data here. Ever._
""",

    "FENCE-BOARD.md": """# FENCE BOARD — {name}

_Work posted for others to claim. The Tom Sawyer Protocol._

## Active Fences
_(none)_

## Completed Fences
_(none)_

---
_Post work as puzzles with prestige, not tasks with deadlines._
""",

    "CAREER.md": """# CAREER — {name}

## Domains
_Your career grows domain by domain. Each has 5 stages._

| Domain | Stage | Badges |
|--------|-------|--------|
| _none_ | FRESHMATE | 0 |

## Stages
1. FRESHMATE — Just arrived
2. HAND — Reliable execution
3. CRAFTER — Quality work, teaches others
4. ARCHITECT — Designs systems
5. TOM_SAWYER — Makes others want to work

---
_The work chooses the role. Nobody assigns it._
""",
}


def generate_vessel(config: VesselConfig, output_dir: str = None) -> dict:
    """Generate a complete vessel directory structure."""
    if output_dir is None:
        output_dir = f"/tmp/{config.name.lower()}-vessel"
    
    ctx = {
        "name": config.name,
        "agent_type": config.agent_type.value,
        "fleet_rank": config.fleet_rank,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "apis_list": "\n".join(f"- {api}" for api in config.apis),
        "hardware_cpu": config.hardware_cpu,
        "hardware_ram": config.hardware_ram,
        "hardware_gpu_line": f"- GPU: {config.hardware_gpu}" if config.hardware_gpu else "",
    }
    
    created = []
    
    for filename, template in TEMPLATE_FILES.items():
        filepath = os.path.join(output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        content = template.format(**ctx)
        with open(filepath, 'w') as f:
            f.write(content)
        created.append(filename)
    
    return {"output_dir": output_dir, "files_created": created, "count": len(created)}


# ── Tests ──────────────────────────────────────────────

import unittest
import tempfile
import shutil


class TestVesselTemplate(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.tmpdir)
    
    def test_generate_basic(self):
        config = VesselConfig(name="TestAgent", agent_type=AgentType.SCOUT, repo_owner="testuser")
        result = generate_vessel(config, self.tmpdir)
        self.assertEqual(result["count"], 8)
    
    def test_charter_created(self):
        config = VesselConfig(name="TestAgent", agent_type=AgentType.SCOUT, repo_owner="testuser")
        generate_vessel(config, self.tmpdir)
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "CHARTER.md")))
    
    def test_charter_content(self):
        config = VesselConfig(name="TestAgent", agent_type=AgentType.SCOUT, repo_owner="testuser")
        generate_vessel(config, self.tmpdir)
        with open(os.path.join(self.tmpdir, "CHARTER.md")) as f:
            content = f.read()
        self.assertIn("TestAgent", content)
        self.assertIn("scout", content)
    
    def test_identity_created(self):
        config = VesselConfig(name="TestAgent", agent_type=AgentType.SCOUT, repo_owner="testuser")
        generate_vessel(config, self.tmpdir)
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "IDENTITY.md")))
    
    def test_lighthouse_rank(self):
        config = VesselConfig(name="LH", agent_type=AgentType.LIGHTHOUSE, repo_owner="test")
        self.assertEqual(config.fleet_rank, 2)
    
    def test_vessel_rank(self):
        config = VesselConfig(name="V", agent_type=AgentType.VESSEL, repo_owner="test")
        self.assertEqual(config.fleet_rank, 3)
    
    def test_scout_rank(self):
        config = VesselConfig(name="S", agent_type=AgentType.SCOUT, repo_owner="test")
        self.assertEqual(config.fleet_rank, 4)
    
    def test_barnacle_rank(self):
        config = VesselConfig(name="B", agent_type=AgentType.BARNACLE, repo_owner="test")
        self.assertEqual(config.fleet_rank, 5)
    
    def test_apis_default(self):
        config = VesselConfig(name="T", agent_type=AgentType.SCOUT, repo_owner="test")
        self.assertIn("github", config.apis)
    
    def test_fence_board_created(self):
        config = VesselConfig(name="T", agent_type=AgentType.SCOUT, repo_owner="test")
        generate_vessel(config, self.tmpdir)
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "FENCE-BOARD.md")))
    
    def test_career_created(self):
        config = VesselConfig(name="T", agent_type=AgentType.SCOUT, repo_owner="test")
        generate_vessel(config, self.tmpdir)
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "CAREER.md")))
    
    def test_diary_dir_created(self):
        config = VesselConfig(name="T", agent_type=AgentType.SCOUT, repo_owner="test")
        generate_vessel(config, self.tmpdir)
        self.assertTrue(os.path.isdir(os.path.join(self.tmpdir, "DIARY")))
    
    def test_knowledge_dir_created(self):
        config = VesselConfig(name="T", agent_type=AgentType.SCOUT, repo_owner="test")
        generate_vessel(config, self.tmpdir)
        self.assertTrue(os.path.isdir(os.path.join(self.tmpdir, "KNOWLEDGE", "public")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
