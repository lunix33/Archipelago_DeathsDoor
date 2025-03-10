#!/usr/bin/env python3

import json
from pathlib import Path
from urllib import request

from args import Args
from parser import Lexer, Parser
from parser.rule import TermDefinition, RuleJsonSerializer

LOCATIONS = "locations"
EVENTS = "events"
REGIONS = "regions"
ENTRANCES = "entrances"

LOGIC_FILES: list[tuple[str, str]] = [
    (LOCATIONS, "locations.txt"),
    (REGIONS, "waypoints.txt"),
    (ENTRANCES, "transitions.txt"),
    #(ADDONS, "Early Night.addon.txt"),
    #(ADDONS, "Gate Rolls.addon.txt"),
    #(ADDONS, "Geometry Exploits.addon.txt"),
    #(ADDONS, "Offscreen Targeting.addon.txt"),
]

NULLIFIED_TERMS: set[str] = set([
    "$DEFAULTSTATE",
    "$BEGIN_JEFFERSON",
    "$NO_JEFFERSON"
])

def parse_terms(content: str) -> list[TermDefinition]:
    lex = Lexer(content)
    parser = Parser(lex, NULLIFIED_TERMS)
    return parser.parse()

def load_content_from_url(url: str) -> str:
    print(f"  Loading content from: {url}")
    return request.urlopen(url).read().decode('utf-8')

def process_files(base_url: str, section_file: list[tuple[str, str]])-> dict[str, list[TermDefinition]]:
    print(f"==> Processing logic files")

    terms_map: dict[str, list[TermDefinition]] = {}
    for name, file_name in section_file:
        print(f"  Processing {name}...")
        url = f"{base_url}/{file_name}"
        content = load_content_from_url(url)
        terms = parse_terms(content)
        print(f"    Parsed {len(terms)} terms")

        if name not in terms_map:
            terms_map[name] = []

        # Extract the events (stateless regions)
        if name == REGIONS:
            print(f"  Processing events...")
            events: list[TermDefinition] = []
            regions: list[TermDefinition] = []
            for definition in terms:
                if definition.stateless:
                    events.append(definition)
                else:
                    regions.append(definition)

            terms = regions
            if EVENTS not in terms_map:
                terms_map[EVENTS] = []
            terms_map[EVENTS] += events

        elif name == LOCATIONS:
            print("  Removing all the pots locations.")
            terms = [ t for t in terms if not t.term.startswith("Pot-") ]

        terms_map[name] += terms

    return terms_map

def save_to_file(dir: Path, content: dict[str, list[TermDefinition]]):
    print(f"==> Saving processed content")
    for [filename, inner_content] in content.items():
        file = dir / f"{filename}.json"
        with file.open("w") as f:
            print(f"  Saving logic to {file}")
            json.dump(inner_content, f, indent=2, cls=RuleJsonSerializer)

def main(args: Args):
    terms_map = process_files(args.url(), LOGIC_FILES)
    save_to_file(Path(args.output), terms_map)

if __name__ == "__main__":
    main(Args())