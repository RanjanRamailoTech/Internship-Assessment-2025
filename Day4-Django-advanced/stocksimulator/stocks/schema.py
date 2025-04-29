# stocks/swagger_schemas.py
from drf_yasg import openapi

# Define the StockPrice response schema
stock_price_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Stock price ID'),
        'company': openapi.Schema(type=openapi.TYPE_STRING, description='Company name'),
        'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='Stock price'),
    },
    required=['id', 'company', 'price']
)

# Define the success response (200)
stock_prices_response = openapi.Response(
    description="List of stock prices",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=stock_price_schema
    )
)

# Define the error response (404)
no_data_response = openapi.Response(
    description="No stock price data available for the current sequence",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
        }
    )
)

# Combine responses for use in swagger_auto_schema
stock_price_api_responses = {
    200: stock_prices_response,
    404: no_data_response
}