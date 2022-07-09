from collections import Counter
from tarantool import space


def run_search_by_caption(fulltext_search_space: space.Space, caption: str) -> int:
    c = Counter()

    for word in caption.split(' '):
        res = fulltext_search_space.select(word.lower(), index='secondary')
        for row in res.data:
            for uid in row[1:]:
                c[uid] += 1

    if len(c) > 0:
        uid = c.most_common(1)[0][0]
        return uid

    return 0
