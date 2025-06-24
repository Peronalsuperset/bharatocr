import re

REDACTION_PATTERNS = [
    ("PAN", re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")),
    ("AADHAAR", re.compile(r"\b[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\b")),
    ("UDYAM", re.compile(r"UDYAM-[A-Z]{2}-\d{2}-\d{7}")),
    ("BANK_AC", re.compile(r"\b\d{9,18}\b")),
]

REDACTED_STR = "[REDACTED]"

def redact_text(text):
    """
    Redacts sensitive data in the text.
    Returns redacted text and a list of (type, match) tuples.
    """
    redacted = text
    found = []
    for label, pattern in REDACTION_PATTERNS:
        for m in pattern.findall(text):
            found.append((label, m))
            redacted = redacted.replace(m, REDACTED_STR)
    return redacted, found

def redact_blocks(layout_blocks):
    """
    Redacts sensitive data in each block's text.
    Returns new blocks and a list of redacted items.
    """
    redacted_blocks = []
    all_found = []
    for block in layout_blocks:
        redacted_text, found = redact_text(block["text"])
        new_block = block.copy()
        new_block["text"] = redacted_text
        redacted_blocks.append(new_block)
        all_found.extend(found)
    return redacted_blocks, all_found 