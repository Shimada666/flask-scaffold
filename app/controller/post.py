from flask import current_app as app

from app.libs.web_response import WebResponse
from app.models.post import Post


@app.route('/api/v1/post', methods=['GET'])
def list_post():
    posts = Post.list()
    return WebResponse.build_data([post.to_dict() for post in posts])
