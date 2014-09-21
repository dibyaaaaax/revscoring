import re

from ..datasources import contiguous_segments_removed
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('[a-zA-Z]+', re.UNICODE)

@depends(on=[contiguous_segments_removed])
@returns(int)
def words_removed(contiguous_segments_removed):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_removed)
