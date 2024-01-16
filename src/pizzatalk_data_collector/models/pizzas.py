import json


class Articles:
    def __init__(
        self, title, content, published_date, featured_image_url, source_url
    ):
        self.title = title
        self.content = content
        self.published_date = published_date
        self.featured_image_url = featured_image_url
        self.source_url = source_url

    def to_json(self):
        return json.dumps(
            {
                "title": self.title,
                "content": self.content,
                "publishedDate": self.published_date,
                "featuredImageURL": self.featured_image_url,
                "sourceURL": self.source_url,
            }
        )

    def __str__(self):
        return f"Articles(title={self.title}, content={self.content}, publishedDate={self.published_date}, featuredImageURL={self.featured_image_url}, sourceURL={self.source_url})"
