from shopify_client import ShopifyClient
import re

class MockLLM:
    """
    Simulates an LLM for the purpose of this assignment.
    In a real app, this would call OpenAI/Claude.
    """
    def generate_plan(self, question):
        question = question.lower()
        if "inventory" in question or "stock" in question:
            return {
                "intent": "inventory_projection",
                "query": "FROM inventory SHOW product_title, quantity WHERE quantity < 10",
                "explanation_template": "Based on current stock levels, the following products are running low: {data}"
            }
        elif "sales" in question or "selling" in question:
            return {
                "intent": "sales_trends",
                "query": "FROM orders SHOW sum(total_price) SINCE -7d",
                "explanation_template": "Your total sales for the last week were {data}."
            }
        elif "customers" in question:
            return {
                "intent": "customer_analysis",
                "query": "FROM customers SHOW count() WHERE orders_count > 1 SINCE -90d",
                "explanation_template": "{data} customers have placed repeat orders in the last 90 days."
            }
        else:
            return {
                "intent": "unknown",
                "query": None,
                "explanation_template": "I'm not sure how to answer that. Try asking about inventory, sales, or customers."
            }

class AnalyticsAgent:
    def __init__(self):
        self.llm = MockLLM()

    def process(self, store_id, question, access_token=None):
        # 1. Understand & Plan (via LLM)
        plan = self.llm.generate_plan(question)
        
        if not plan["query"]:
            return {
                "answer": plan["explanation_template"],
                "confidence": "low"
            }

        # 2. Validate Query Correctness
        if not self._validate_query(plan["query"]):
            return {
                "answer": "I generated a query but it didn't pass my safety checks. Please try rephrasing.",
                "confidence": "low"
            }

        # 3. Execute
        client = ShopifyClient(store_id, access_token)
        raw_data = client.execute_shopify_ql(plan["query"])
        
        # 3. Explain (Post-processing)
        # Extracting data from mock response structure
        rows = raw_data.get("data", {}).get("table", {}).get("rows", [])
        
        if not rows:
            answer = "I couldn't find any data matching your request."
        else:
            # Simple formatter
            formatted_data = self._format_data(rows, plan["intent"])
            answer = plan["explanation_template"].format(data=formatted_data)

        return {
            "answer": answer,
            "confidence": "high",
            "sql_generated": plan["query"]
        }

    def _format_data(self, rows, intent):
        if intent == "inventory_projection":
            # rows might be [['Product A', 10], ['Product B', 5]]
            items = [f"{r[0]} ({r[1]} units)" for r in rows]
            return ", ".join(items)
        elif intent == "sales_trends":
            # rows might be [[5000.0]]
            return f"${rows[0][0]}"
        elif intent == "customer_analysis":
            # rows might be [[150]]
            return str(rows[0][0])
        return str(rows)

    def _validate_query(self, query):
        """
        Validates the generated ShopifyQL.
        In a real app, this would check against a schema or use a parser.
        """
        required_keywords = ["FROM", "SHOW"]
        forbidden_keywords = ["DROP", "DELETE", "INSERT", "UPDATE"] # Security bridge
        
        query_upper = query.upper()
        
        # Check basic syntax
        if not all(kw in query_upper for kw in required_keywords):
            return False
            
        # Security check
        if any(kw in query_upper for kw in forbidden_keywords):
            return False
            
        return True
