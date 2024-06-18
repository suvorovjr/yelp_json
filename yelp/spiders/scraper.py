import json
import scrapy
from typing import Iterable
from dateutil import parser
from scrapy import Request
from ..items import ReviewItem, AnswerItem, OwnerAnswerItem


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
        reviews = response_data['data']['business']['reviews']['edges']
        for item in reviews:
            review = ReviewItem()
            review['author'] = item['node']['author']['displayName']
            review['review_text'] = item['node']['text']['full']
            review['stars'] = item['node']['rating']
            review['date'] = parser.parse(item['node']['createdAt']['localDateTimeForBusiness'])
            if len(item['node']['businessPhotos']) >= 1:
                photo_urls = []
                for photo in item['node']['businessPhotos']:
                    photo_url = photo['photoUrl']['url']
                    photo_urls.append(photo_url)
                review['photo_urls'] = photo_urls
            if len(item['node']['previousReviews']) >= 1:
                review['answers'] = []
                for subitem in item['node']['previousReviews']:
                    answer = AnswerItem()
                    answer['answer_username'] = subitem['author']['displayName']
                    answer['answer_text'] = subitem['text']['full']
                    answer['answer_date'] = subitem['createdAt']['localDateTimeForBusiness']
                    answer['answer_stars'] = subitem['rating']
                    review['answers'].append(answer)

            yield review

        next_page = response_data['data']['business']['reviews']['pageInfo']['hasNextPage']
        this_page = response_data['data']['business']['reviews']['pageInfo']['endCursor']
        yield response_data

    @staticmethod
    def get_json_data(after=None):
        json_data = {
            'operationName': 'GetBusinessReviewFeed',
            'variables': {
                'encBizId': 'JHQPPOksb_iMklR0NAeZUQ',
                'reviewsPerPage': 20,
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
