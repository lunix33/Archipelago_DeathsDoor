#!/usr/bin/env python3

import json
from pathlib import Path
from urllib import request

from args import Args
from parser import Lexer, Parser
from parser.rule import TermDefinition, RuleJsonSerializer

LOGIC_FILES: list[str] = [
    "locations.txt",
    "waypoints.txt",
    "transitions.txt",
    #"Early Night.addon.txt",
    #"Gate Rolls.addon.txt",
    #"Geometry Exploits.addon.txt",
    #"Offscreen Targeting.addon.txt"
]

def parse_terms(content: str) -> list[TermDefinition]:
    lex = Lexer(content)
    parser = Parser(lex)
    return parser.parse()

def load_content_from_url(url: str) -> str:
    print(f"==> Loading content from: {url}")
    return request.urlopen(url).read().decode('utf-8')

def main(args: Args):
    terms_map: dict[str, list[TermDefinition]] = {}
    for file_name in LOGIC_FILES:
        url = f"{args.url()}/{file_name}"
        content = load_content_from_url(url)
        terms = parse_terms(content)
        terms_map[file_name] = terms

    file = Path(args.output)
    with file.open("w+") as f:
        print(f"==> Saving logic to {file}")
        json.dump(terms_map, f, indent=2, cls=RuleJsonSerializer)

if __name__ == "__main__":
    main(Args())