from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_URL = "https://fakestoreapi.com/products"


def fetch_products():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        return None  


def get_product_details(product_name: str) -> str:
    products = fetch_products()

    if not products:  
        return "Sorry, I couldn't retrieve product information at the moment."

    if isinstance(product_name, list): 
        product_name = product_name[0]

    for product in products:
        if product_name.lower() in product["title"].lower():
            return (
                f"ID: {product['id']}\n"
                f"Title: {product['title']}\n"
                f"Price: ${product['price']}\n"
                f"Description: {product['description']}\n"
                f"Category: {product['category']}\n"
                f"Rating: {product['rating']['rate']}"
            )
    return "Sorry, I couldn't find a product matching your description."


class DialogflowRequest(BaseModel):
    queryResult: dict


@app.get("/")
async def root():
    return {"message": "Chatbot webhook is running!"}


@app.post("/webhook")
async def webhook(req: DialogflowRequest):
    intent_name = req.queryResult["intent"]["displayName"]

    if intent_name == "Product_Inquiry":
        product_name = req.queryResult["parameters"].get("product_name")
        product_details = get_product_details(product_name)
        return {"fulfillmentText": product_details}

    elif intent_name == "Bargaining":
        user_response = req.queryResult["queryText"]
        price = req.queryResult["parameters"].get("price", 100) 
        discount = 0.10  # 10% discount
        discounted_price = round(float(price) * (1 - discount), 2)

        if any(keyword in user_response.lower() for keyword in ["more discount", "more", "discount", "sale", "offer"]):
            return {"fulfillmentText": f"How about a 10% discount? Final price is ${discounted_price}."}
        return  {"fulfillmentText": f"How about a 10% discount? Final price is ${discounted_price} It's a great deal!"}

    elif intent_name == "Order_Tracking":
        order_id = req.queryResult["parameters"].get("id")
        product_name = req.queryResult["parameters"].get("product_name")
        if order_id and product_name:
            return {"fulfillmentText": f"Your order of {product_name} with ID {order_id} is on the way!"}
        return {"fulfillmentText": "Please provide both order ID and product name for tracking."}

    return {"fulfillmentText": "Sorry, I didn't understand that."}

