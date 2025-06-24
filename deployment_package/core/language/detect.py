from langdetect import detect, DetectorFactory, LangDetectException
from langdetect import detect_langs

# Make language detection deterministic
DetectorFactory.seed = 0

def detect_language(text):
    """
    Detects the primary language of the given text.
    Returns a language code (e.g., 'en', 'hi').
    """
    try:
        return detect(text)
    except LangDetectException:
        return None

def detect_language_probs(text):
    """
    Returns a list of (lang, prob) tuples for the text.
    """
    try:
        return [(l.lang, l.prob) for l in detect_langs(text)]
    except LangDetectException:
        return [] 