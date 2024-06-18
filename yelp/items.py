# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewItem(scrapy.Item):
    author = scrapy.Field()
    review_text = scrapy.Field()
    stars = scrapy.Field()
    date = scrapy.Field()
    photo_urls = scrapy.Field()
    answers = scrapy.Field()
    owner_answers = scrapy.Field()


class AnswerItem(scrapy.Item):
    pass


class OwnerAnswerItem(scrapy.Item):
    pass
