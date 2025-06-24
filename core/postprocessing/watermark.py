import math

WATERMARK_WORDS = ["draft", "copy", "sample", "specimen"]
ANGLE_THRESHOLD_DEGREES = 10  # If angle deviates from 0/90 by more than this, flag as watermark

def is_rotated(bbox):
    # bbox: [x0, y0, x1, y1] (assume horizontal if y0==y1)
    x0, y0, x1, y1 = bbox
    dx = x1 - x0
    dy = y1 - y0
    angle = math.degrees(math.atan2(dy, dx))
    # Normalize angle to [0, 180)
    angle = abs(angle) % 180
    # Check if angle is not close to 0 or 90
    if min(abs(angle), abs(angle-90)) > ANGLE_THRESHOLD_DEGREES:
        return True
    return False

def is_watermark_text(text):
    t = text.lower()
    return any(w in t for w in WATERMARK_WORDS)

def flag_watermark_blocks(layout_blocks):
    """
    Returns a list of indices of blocks flagged as watermark.
    """
    flagged = []
    for i, block in enumerate(layout_blocks):
        if is_rotated(block["bbox"]) or is_watermark_text(block["text"]):
            flagged.append(i)
    return flagged 