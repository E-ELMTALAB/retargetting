import re
from pathlib import Path
import sys

TOKEN_REGEX = re.compile(r"\b\d{16}-[A-Z]{4}-[A-Za-z0-9]{10}\b")


def extract_tokens(input_path: str = "pro_codes.txt", output_path: str = "pro_codes_clean.txt") -> int:
    """Read the input file, extract unique tokens using TOKEN_REGEX,
    and write them one per line into the output file.
    Returns the number of tokens written."""
    try:
        text = Path(input_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Input file '{input_path}' not found.")
        return 0

    tokens = TOKEN_REGEX.findall(text)
    unique_tokens = sorted(set(tokens))
    Path(output_path).write_text("\n".join(unique_tokens), encoding="utf-8")
    return len(unique_tokens)


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "pro_codes.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "pro_codes_clean.txt"
    count = extract_tokens(in_file, out_file)
    print(f"Wrote {count} clean tokens to '{out_file}'.")
