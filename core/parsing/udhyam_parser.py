import re

UDYAM_FIELDS = [
    ("udyam_number", r"Udyam Registration Number\s*[:\-]?\s*([A-Z0-9\-]+)", re.I),
    ("enterprise_name", r"Name of Enterprise\s*[:\-]?\s*([A-Za-z0-9\s\.,&'-]+)", re.I),
    ("owner_name", r"Name of Owner\s*[:\-]?\s*([A-Za-z0-9\s\.,&'-]+)", re.I),
    ("type_of_organization", r"Type of Organization\s*[:\-]?\s*([A-Za-z\s]+)", re.I),
    ("date_of_commencement", r"Date of Commencement\s*[:\-]?\s*([0-9\-/]+)", re.I),
]

def parse_udhyam(text):
    """
    Parses the text for Udyam Certificate fields.
    Returns a dict of field_name: value.
    """
    result = {}
    for field, pattern, flags in UDYAM_FIELDS:
        match = re.search(pattern, text, flags)
        if match:
            result[field] = match.group(1).strip()
    return result 