from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .schemas import Persona, Scenario, TagTaxonomy


def _read_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_persona(path: str | Path) -> Persona:
    return Persona.model_validate(_read_yaml(path))


def load_scenario(path: str | Path) -> Scenario:
    return Scenario.model_validate(_read_yaml(path))


def load_tag_taxonomy(path: str | Path) -> TagTaxonomy:
    return TagTaxonomy.model_validate(_read_yaml(path))
