from drf_yasg import openapi

FETCH_STOCK_API = {
    "operation_description": "Fetch and update current stock data from external source.",
    "responses": {
        201: openapi.Response(
            description="Stock data updated",
            examples={
                "application/json": {
                    "status-code": 1,
                    "status-message": "",
                    "data": {"message": "Stock data updated"}
                }
            }
        ),
        500: openapi.Response(
            description="Fetch failed",
            examples={
                "application/json": {
                    "status-code": -1,
                    "status-message": "",
                    "data": {"message": "Connection error"}
                }
            }
        )
    }
}

STOCK_LIST_API = {
    "operation_description": "List all stocks with current prices.",
    "responses": {
        200: openapi.Response(
            description="List of stocks",
            examples={
                "application/json": {
                    "status-code": 1,
                    "status-message": "",
                    "data": [
                        {"id": 1, "company_name": "ABC", "current_price": "123.4500"},
                        {"id": 2, "company_name": "XYZ", "current_price": "456.7800"}
                    ]
                }
            }
        )
    }
}

STOCK_DETAIL_API = {
    "operation_description": "Get details of a specific stock by ID.",
    "manual_parameters": [
        openapi.Parameter("stock_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="Stock ID")
    ],
    "responses": {
        200: openapi.Response(
            description="Stock details",
            examples={
                "application/json": {
                    "status-code": 1,
                    "status-message": "",
                    "data": {"id": 1, "company_name": "ABC", "current_price": "123.4500"}
                }
            }
        ),
        404: openapi.Response(
            description="Stock not found",
            examples={
                "application/json": {
                    "status-code": -1,
                    "status-message": "",
                    "data": {"message": "Stock not found"}
                }
            }
        )
    }
}