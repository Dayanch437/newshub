"""Interface text in English and Turkmen.

Kept as a dict instead of gettext .po files so the project needs no system packages.
"""

UI_TEXT = {
    'tagline': {
        'en': 'AI summaries of world, tech and Central Asia news',
        'tk': 'Dünýä, tehnologiýa we Merkezi Aziýa habarlarynyň AI gysgaça mazmuny',
    },
    'latest': {'en': 'Latest news', 'tk': 'Soňky habarlar'},
    'all': {'en': 'All', 'tk': 'Hemmesi'},
    'search_placeholder': {'en': 'Search news…', 'tk': 'Habarlary gözle…'},
    'search': {'en': 'Search', 'tk': 'Gözle'},
    'results_for': {'en': 'Results for', 'tk': 'Gözleg netijeleri:'},
    'all_sources': {'en': 'All sources', 'tk': 'Ähli çeşmeler'},
    'source': {'en': 'Source', 'tk': 'Çeşme'},
    'tags': {'en': 'Tags', 'tk': 'Bellikler'},
    'read_original': {'en': 'Read the original article', 'tk': 'Asyl makalany oka'},
    'back': {'en': 'Back to news', 'tk': 'Habarlara dolan'},
    'no_news': {'en': 'No news yet.', 'tk': 'Entek habar ýok.'},
    'no_summary': {'en': 'Summary is not ready yet.', 'tk': 'Gysgaça mazmun entek taýýar däl.'},
    'tk_pending': {
        'en': '',
        'tk': 'Terjime entek taýýar däl — iňlis dilinde görkezilýär.',
    },
    'previous': {'en': 'Previous', 'tk': 'Öňki'},
    'next': {'en': 'Next', 'tk': 'Indiki'},
    'page': {'en': 'Page', 'tk': 'Sahypa'},
    'of': {'en': 'of', 'tk': '/'},
}


def ui(key, lang):
    entry = UI_TEXT.get(key, {})
    return entry.get(lang) or entry.get('en', key)
