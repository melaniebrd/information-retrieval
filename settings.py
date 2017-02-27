# CACM collection constants
CACM = "cacm"
CACM_PATH = "data/CACM/cacm.all"
CACM_QUERY_PATH = "data/CACM/query.text"
CACM_QUERY_RESULT_PATH = "data/CACM/qrels.text"

# CS276 collection constants
CS276 = "cs276"
CS276_PATH = "data/CS276/pa1-data"

# CACM Linguistic Process
INITIAL_MARKER = 'I'
TITLE_MARKER = 'T'
QUERY_MARKER = 'W'
MARKERS_TO_CHECK = [INITIAL_MARKER, TITLE_MARKER, 'W', 'K']
MARKERS = MARKERS_TO_CHECK + ['B', 'A', 'N', 'X']
PREFIX = "."

# Index
DOC_IDS_PATH = "doc_ids"
TERM_IDS_PATH = "term_ids"
INDEX_PATH = "index"