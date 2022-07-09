import base64
import os
import tarantool

from flask import abort, Flask, request, Response
from random import randint

from memelib import create_meme

# image_space = box.schema.space.create('image_space')
# image_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
# caption_space = box.schema.space.create('caption_space')
# caption_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
# fulltext_search_space = box.schema.space.create('fulltext_search_space')
# fulltext_search_space:create_index('primary', {parts = {1, 'string', is_nullable=false}})

server = tarantool.connect("localhost", 3301)

image_space = server.space('image_space')
caption_space = server.space('caption_space')
fulltext_search_space = server.space('fulltext_search_space')

app = Flask(__name__)


@app.route("/get/<meme_id>")
def get_handler(meme_id):
    t = image_space.select(int(meme_id))

    img = base64.b64decode(str(t.data[0][1]))
    return Response(img, mimetype='image/png')


@app.route("/set", methods=['POST'])
def set_handler():
    image = request.files.get("image")
    if not image:
        abort(400)

    image.stream.seek(0)
    f = image.stream.read()

    original = base64.b64encode(f).decode("utf-8")
    upper_text = request.form.get("upper_text", "")
    lower_text = request.form.get("lower_text", "")
    meme = create_meme(original, upper_text, lower_text)

    uid = randint(1, 10000000)

    image_space.insert((uid, meme, original))
    caption_space.insert((uid, upper_text, lower_text))

    full_caption = (upper_text + " " + lower_text).strip().split(' ')
    for word in full_caption:
        fulltext_search_space.insert((word, uid))

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
        fulltext_search_space.insert((word, uid))

    return str(uid), 200


if __name__ == "__main__":
    debug = False if os.getenv("ENV") == "PRODUCTION" else True
    app.run(host="0.0.0.0", port=8000, debug=debug)
