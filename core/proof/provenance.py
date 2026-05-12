from dataclasses import dataclass

@dataclass
class Provenance:
    source: str
    source_id: str
    details: dict
