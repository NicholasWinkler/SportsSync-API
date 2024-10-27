# views/news.py
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import urllib.request
import urllib.parse
import json

class NewsAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            search_query = request.query_params.get('search', '')

            # Sources to exclude
            excluded_sources = [
                'betting', 'bet365', 'draftkings', 'fanduel', 'caesars',
                'politics', 'biztoc', 'newsweek', 'time.com',
                'yahoo entertainment', 'freerepublic'
            ]

            # Keywords to filter out
            excluded_keywords = [
                'betting', 'promo code', 'odds', 'gambling',
                'biden', 'trump', 'politics', 'election',
                'bonus', 'bet', 'wager', 'casino',
                'promo', 'promotion', 'sportsbook', 'presidental', 'removed'
            ]

            # Build the query parameters
            params = {
                'apiKey': settings.NEWS_API_KEY,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 100,  # Request more to ensure we have enough after filtering
                'q': f'NBA {search_query}'.strip()
            }

            # Construct the URL with parameters
            query_string = urllib.parse.urlencode(params)
            url = f'https://newsapi.org/v2/everything?{query_string}'
            
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            req = urllib.request.Request(url=url, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                filtered_articles = []
                seen_urls = set()  # Track unique URLs
                
                for article in data.get('articles', []):
                    if not article.get('title') or not article.get('description'):
                        continue

                    url = article.get('url', '').strip()
                    # Skip if we've seen this URL already
                    if url in seen_urls:
                        continue

                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    source = article.get('source', {}).get('name', '').lower()

                    # Skip if from excluded source
                    if any(ex_source in source for ex_source in excluded_sources):
                        continue

                    # Skip if contains excluded keywords
                    if any(keyword in title or keyword in description 
                          for keyword in excluded_keywords):
                        continue

                    seen_urls.add(url)
                    filtered_articles.append({
                        'id': url,
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'url': url,
                        'image_url': article.get('urlToImage'),
                        'published_at': article.get('publishedAt'),
                        'source': article.get('source', {}).get('name')
                    })

                # Sort by published date (newest first) and return top 11
                filtered_articles.sort(key=lambda x: x['published_at'], reverse=True)
                
                return Response({
                    'articles': filtered_articles[:11]
                })
                
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return Response({
                'articles': []
            })