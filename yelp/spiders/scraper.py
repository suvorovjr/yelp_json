from typing import Iterable

import scrapy
import json

from scrapy import Request


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    start_urls = ["https://www.yelp.com/gql/batch"]

    def start_requests(self) -> Iterable[Request]:
        url = 'https://www.yelp.com/gql/batch'
        json_data = ScraperSpider.get_json_data()
        yield scrapy.Request(
            url=url,
            method='POST',
            body=json_data,
            headers={'Content-Type': 'application/json'},
            callback=self.parse_reviews
        )

    def parse_reviews(self, response):
        response_data = json.loads(response.text)
        yield response_data

    @staticmethod
    def get_json_data(after=None):
        json_data = {
            'operationName': 'GetBusinessReviewFeed',
            'variables': {
                'encBizId': 'JHQPPOksb_iMklR0NAeZUQ',
                'reviewsPerPage': 10,
                'selectedReviewEncId': '',
                'hasSelectedReview': False,
                'sortBy': 'DATE_DESC',
                'languageCode': 'en',
                'isSearching': False,
                'after': after,
                'isTranslating': False,
                'translateLanguageCode': 'en',
                'reactionsSourceFlow': 'businessPageReviewSection',
                'minConfidenceLevel': 'HIGH_CONFIDENCE',
                'highlightType': '',
                'highlightIdentifier': '',
                'isHighlighting': False,
            },
            'extensions': {
                'operationType': 'query',
                'documentId': '8bad289146c687e874539832a54eecc102ed2f128ae88c1a2f76b3163538c388',
            },
        }
        return json.dumps(json_data)
