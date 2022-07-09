from collections import Counter
from random import randint

from tarantool import space
from tarantool import const


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


def get_random_caption(caption_space: space.Space) -> (str, str):
    random_id = randint(1, 10000000)

    res = caption_space.select(random_id, limit=1, iterator=const.ITERATOR_GE)
    if len(res.data) > 0:
        return res.data[0][1], res.data[0][2]

    res = caption_space.select(random_id, limit=1, iterator=const.ITERATOR_LE)
    if len(res.data) > 0:
        return res.data[0][1], res.data[0][2]

    return "", ""


def get_random_image(image_space: space.Space) -> (str, str):
    random_id = randint(1, 10000000)

    res = image_space.select(random_id, limit=1, iterator=const.ITERATOR_GE)
    if len(res.data) > 0:
        return res.data[0][1], res.data[0][2]

    res = image_space.select(random_id, limit=1, iterator=const.ITERATOR_LE)
    if len(res.data) > 0:
        return res.data[0][1], res.data[0][2]

    return "", ""
