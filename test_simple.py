#!/usr/bin/env python3
"""Test a simple question."""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from interactive_agent import InteractiveCVAgent

agent = InteractiveCVAgent()
response = agent.chat("What connection exists between Vaios's theoretical work and his practical game development?")
print(f"Response:\n{response}")