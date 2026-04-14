"""
Parses SARIF 2.1.0 reports from Phase 1 into structured RaceCandidate objects.
"""
import json
from pathlib import Path
from typing import List
from models import RaceCandidate, RaceType, ProtectionStatus


def parse_sarif(sarif_path: str) -> List[RaceCandidate]:
    """Parse a SARIF file and extract race candidates."""
    with open(sarif_path, 'r') as f:
        sarif = json.load(f)

    candidates = []

    for run in sarif.get("runs", []):
        for result in run.get("results", []):
            candidate = _parse_result(result)
            if candidate:
                candidates.append(candidate)

    return candidates


def _parse_result(result: dict) -> RaceCandidate:
    """Parse a single SARIF result into a RaceCandidate."""
    props = result.get("properties", {})
    message = result.get("message", {}).get("text", "")

    # Extract race type from rule ID or properties
    race_type_str = props.get("raceType", "")
    if race_type_str == "WRITE_WRITE":
        race_type = RaceType.WRITE_WRITE
    else:
        race_type = RaceType.READ_WRITE

    # Extract protection status
    protection_str = props.get("protectionStatus", "UNPROTECTED")
    try:
        protection = ProtectionStatus(protection_str)
    except ValueError:
        protection = ProtectionStatus.UNPROTECTED

    # Extract locations
    locations = result.get("locations", [])
    related_locations = result.get("relatedLocations", [])

    source_file_1 = ""
    line_1 = 0
    if locations:
        loc = locations[0]
        phys = loc.get("physicalLocation", {})
        source_file_1 = phys.get("artifactLocation", {}).get("uri", "")
        line_1 = phys.get("region", {}).get("startLine", 0)

    source_file_2 = ""
    line_2 = 0
    if related_locations:
        rloc = related_locations[0]
        phys = rloc.get("physicalLocation", {})
        source_file_2 = phys.get("artifactLocation", {}).get("uri", "")
        line_2 = phys.get("region", {}).get("startLine", 0)

    # Parse endpoint names from properties
    ep1_str = props.get("endpoint1", "")
    ep2_str = props.get("endpoint2", "")

    # Extract endpoint name (format: "GET /path (Class.method)")
    ep1_name = _extract_endpoint_name(ep1_str)
    ep2_name = _extract_endpoint_name(ep2_str)
    ep1_http = _extract_http(ep1_str)
    ep2_http = _extract_http(ep2_str)

    severity = "CRITICAL" if result.get("level") == "error" else "HIGH"

    return RaceCandidate(
        entity=props.get("entity", ""),
        endpoint1_name=ep1_name,
        endpoint2_name=ep2_name,
        endpoint1_http=ep1_http,
        endpoint2_http=ep2_http,
        race_type=race_type,
        severity=severity,
        protection_status=protection,
        source_file_1=source_file_1,
        source_file_2=source_file_2,
        line_number_1=line_1,
        line_number_2=line_2,
        description=message
    )


def _extract_endpoint_name(ep_str: str) -> str:
    """Extract 'Class.method' from 'GET /path (Class.method)'"""
    if "(" in ep_str and ")" in ep_str:
        return ep_str[ep_str.index("(") + 1:ep_str.index(")")]
    return ep_str


def _extract_http(ep_str: str) -> str:
    """Extract 'GET /path' from 'GET /path (Class.method)'"""
    if "(" in ep_str:
        return ep_str[:ep_str.index("(")].strip()
    return ep_str
