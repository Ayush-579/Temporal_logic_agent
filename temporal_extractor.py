import re
import csv
from typing import List, Dict, Any

PATTERNS = {
    "absolute_date": re.compile(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s+\d{4})?",
        re.IGNORECASE,
    ),
    "relative": re.compile(
        r"\b(\d+)\s*(day|days|weeks|months|years)\s*(after|before|from|within|following)\b",
        re.IGNORECASE,
    ),
    "conditional": re.compile(
        r"\b(upon|after|when|if|once|following|pending)\s+(?:government\s+|presidential\s+)?(?:certification|approval|authorization|compliance)\b",
        re.IGNORECASE,
    ),
    "recurring": re.compile(
        r"\b(quarterly|annually?|monthly|weekly|daily|every\s+quarter|every\s+year)\b",
        re.IGNORECASE,
    ),
    "sunset": re.compile(
        r"\b(expires?|terminates?|ends?|lapses?)\s*(on|after|upon)?\s*([^\.]+)",
        re.IGNORECASE,
    ),
    "grace_period": re.compile(
        r"\b(\d+)\s*-?\s*day\s*(grace\s*)?period\b",
        re.IGNORECASE,
    ),
}

def extract_temporal_expressions(input_path: str = "input.txt",
                                 out_csv: str = "temporal_expressions.csv") -> int:
    rows: List[Dict[str, Any]] = []

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    topic = "GLOBAL"
    topic_re = re.compile(r"^(SECTION\s+\d+|[0-9]{1,2}\.[0-9a-zA-Z]+)")

    for i, line in enumerate(lines):
        stripped = line.strip()
        m_top = topic_re.match(stripped)
        if m_top:
            topic = m_top.group(1)

        for ttype, pat in PATTERNS.items():
            for m in pat.finditer(line):
                rows.append(
                    {
                        "line_number": i,
                        "topic_context": topic,
                        "expression_type": ttype,
                        "raw_text": m.group(0).strip(),
                        "normalized_value": m.group(0).strip(),
                    }
                )

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "line_number",
                "topic_context",
                "expression_type",
                "raw_text",
                "normalized_value",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)

if __name__ == "__main__":
    n = extract_temporal_expressions()
    print(f"Extracted {n} temporal expressions into temporal_expressions.csv")
