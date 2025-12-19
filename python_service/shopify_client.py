import requests
import json

class ShopifyClient:
    def __init__(self, store_id, access_token=None):
        self.store_id = store_id
        self.access_token = access_token or "mock_token"
        self.base_url = f"https://{store_id}/admin/api/2023-10/graphql.json"

    def execute_shopify_ql(self, query):
        """
        Executes a ShopifyQL query.
        In a real scenario, this would hit the Shopify Analytics API.
        Here we mock responses based on the query content.
        """
        print(f"Executing ShopifyQL: {query}")
        
        # Mocking responses for demonstration
        if "orders" in query.lower() and "count" in query.lower():
             return {"data": {"table": {"rows": [[150]]}}} # 150 orders
        
        if "total_price" in query.lower():
             return {"data": {"table": {"rows": [[5000.00]]}}} # $5000 sales
             
        if "inventory" in query.lower():
             return {"data": {"table": {"rows": [["Product A", 10], ["Product B", 5]]}}}

        return {"data": {"table": {"rows": []}}}

    def get_products(self):
        # Mock product data
        return [
            {"id": 1, "title": "Red T-Shirt", "inventory": 20},
            {"id": 2, "title": "Blue Jeans", "inventory": 5},
            {"id": 3, "title": "Sneakers", "inventory": 0}
        ]
