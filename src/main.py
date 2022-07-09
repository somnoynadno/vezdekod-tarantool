import base64
import os
import tarantool

from flask import abort, Flask, request, Response, render_template
from random import randint

from memelib import create_meme
from memelib import get_most_frequent_color
from memelib import replace_color_with_vk_color

from searches import run_search_by_caption
from searches import get_random_caption
from searches import get_random_image

# image_space = box.schema.space.create('image_space')
# image_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
# caption_space = box.schema.space.create('caption_space')
# caption_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
# fulltext_search_space = box.schema.space.create('fulltext_search_space')
# fulltext_search_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
# fulltext_search_space:create_index('secondary', {unique = false, parts = {2, 'string', is_nullable=false}})

server = tarantool.connect("localhost", 3301)

image_space = server.space('image_space')
caption_space = server.space('caption_space')
fulltext_search_space = server.space('fulltext_search_space1')

app = Flask(__name__)


@app.route("/")
def index_handler():
    _, original = get_random_image(image_space)
    upper_text, lower_text = get_random_caption(caption_space)
    image = create_meme(original, upper_text, lower_text)

    return render_template('index.html', base64_image=image)


@app.route("/get/<meme_id>")
def get_handler(meme_id):
    t = image_space.select(int(meme_id))
    if len(t.data) == 0:
        abort(404)

    img = base64.b64decode(str(t.data[0][1]))
    return Response(img, mimetype='image/png')


@app.route("/set", methods=['POST'])
def set_handler():
    image = request.files.get("image")
    upper_text = request.form.get("upper_text", "")
    lower_text = request.form.get("lower_text", "")
    vk_style = request.form.get("vk_style", False)

    if not upper_text and not lower_text:
        upper_text, lower_text = get_random_caption(caption_space)

    if not image:
        uid = run_search_by_caption(fulltext_search_space, upper_text + " " + lower_text)
        if uid == 0:
            return "can't find suitable image in database, please provide one =(", 500

        t = image_space.select(int(uid))
        if len(t.data) == 0:
            abort(404)

        original = t.data[0][2]
    else:
        image.stream.seek(0)
        f = image.stream.read()

        original = base64.b64encode(f).decode("utf-8")

    meme = create_meme(original, upper_text, lower_text)

    if vk_style:
        frequent_color = get_most_frequent_color(meme)
        meme = replace_color_with_vk_color(meme, frequent_color)

    uid = randint(1, 10000000)

    image_space.insert((uid, meme, original))
    caption_space.insert((uid, upper_text, lower_text))

    full_caption = (upper_text + " " + lower_text).strip().split(' ')
    for word in full_caption:
        row_id = randint(1, 1000000000)
        fulltext_search_space.insert((row_id, word.lower(), uid))

    return str(uid), 200


@app.route("/set/json", methods=['POST'])
def set_json_handler():
    j = request.json
    original = j.get("image")
    if not original:
        abort(400)

    upper_text = j.get("upper_text", "")
    lower_text = j.get("lower_text", "")
    meme = create_meme(original, upper_text, lower_text)

    uid = randint(1, 10000000)
    image_space.insert((uid, meme, original))
    caption_space.insert((uid, upper_text, lower_text))

    full_caption = (upper_text + " " + lower_text).strip().split(' ')
    for word in full_caption:
        row_id = randint(1, 1000000000)
        fulltext_search_space.insert((row_id, word.lower(), uid))

    return str(uid), 200


if __name__ == "__main__":
    debug = False if os.getenv("ENV") == "PRODUCTION" else True
    app.run(host="0.0.0.0", port=8000, debug=debug)
