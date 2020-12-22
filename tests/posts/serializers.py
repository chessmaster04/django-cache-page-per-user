def serialize_post(post):
    return {
        'id': post.id,
        'author_id': post.author_id,
        'text': post.text,
    }
