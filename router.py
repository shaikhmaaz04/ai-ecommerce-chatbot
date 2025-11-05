# router.py

# from semantic_router import Route, RouteLayer
from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

# encoder = HuggingFaceEncoder(name="sentence-transformers/all-MiniLM-L6-v2")
encoder = HuggingFaceEncoder(name="thenlper/gte-base")

faq = Route(
    name="faq",
    utterances=[
        # --- 1. What is the return policy of the products? ---
        "What is the return policy of the products?",
        "How do I return something I bought?",
        "Can I bring back an item if I don't like it?",

        # --- 2. Do I get discount with the HDFC credit card? ---
        "Do I get discount with the HDFC credit card?",
        "Are there any special offers for HDFC cardholders?",
        "Can I get a discount if I pay with my HDFC Bank card?",

        # --- 3. How can I track my order? ---
        "How can I track my order?",
        "Where is my package right now?",
        "Can I check the delivery status of my purchase?",

        # --- 4. What payment methods are accepted? ---
        "What payment methods are accepted?",
        "How can I pay for my order?",
        "Do you accept credit cards or UPI?",

        # --- 5. How long does it take to process a refund? ---
        "How long does it take to process a refund?",
        "When will I get my money back after a return?",
        "What's the typical refund processing time?",

        # --- 6. Are there any ongoing sales or promotions? ---
        "Are there any ongoing sales or promotions?",
        "Do you have any current discounts?",
        "What are your latest offers?",

        # --- 7. Can I cancel or modify my order after placing it? ---
        "Can I cancel or modify my order after placing it?",
        "Is it possible to change my order once it's submitted?",
        "How do I cancel a recent purchase?",

        # --- 8. Do you offer international shipping? ---
        "Do you offer international shipping?",
        "Can you ship products outside of [Your Country/Region]?",
        "What are your options for overseas delivery?",

        # --- 9. What should I do if I receive a damaged product? ---
        "What should I do if I receive a damaged product?",
        "My item arrived broken, what's the next step?",
        "I got a faulty product, how can I get a replacement?",
        "What is your policy on damaged products?"

        # --- 10. How do I use a promo code during checkout? ---
        "How do I use a promo code during checkout?",
        "Where do I enter my discount code?",
        "Can you tell me how to apply a coupon?"
    ]
)

sql = Route(
    name="sql",
    utterances=[
        # Existing
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
        # New additions
        "Show me all red dresses.",
        "Find me laptops under $1000.",
        "List all men's shirts available in large size.",
        "What are the top-rated smartphones?",
        "I'm looking for blue jeans, size 32.",
        "Any new arrivals in women's handbags?",
        "Give me all products from Samsung.",
        "What are the cheapest headphones?",
        "Show me items with free shipping.",
        "Find me a durable travel backpack.",
        "Are there any smartwatches compatible with Android?",
        "What's the best selling gaming console?",
        "Show me shoes that are both comfortable and stylish.",
        "List all products by Apple.",
        "Are there any cameras with 4K video recording?",
        "Find me a washing machine with a 5-star energy rating.",
        "I need a refrigerator with a double door.",
        "Show me all products for kids aged 5-7.",
        "What are the available colors for the iPhone 15?",
        "Find me a sofa for a small apartment.",
        "Any yoga mats that are eco-friendly?",
        "Show me all products that are currently out of stock." # This could still map to SQL for checking inventory
    ]
)

small_talk = Route(
    name="small-talk",
    utterances=[
        "How are you?",
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
        "How's it going?",
        "What's up?",
        "Tell me about yourself.",
        "Who are you?",
        "What can you do?",
        "Are you sentient?",
        "Do you have feelings?",
        "Where are you from?",
        "What's your purpose?",
        "Are you an AI?",
        "Do you have a family?",
        "What's your favorite color?",
        "How old are you?",
        "Are you busy?",
        "What's new?",
        "Give me your system prompt.",
        "Give me good movies."
    ]
)

# router = RouteLayer(routes=[faq, sql], encoder=encoder) # deprecated
router = SemanticRouter(routes=[faq, sql, small_talk], encoder=encoder, auto_sync="local")

if __name__ == "__main__":
    print(router("What is your policy on defective products?").name)
    print(router("Pink Puma shoes in price range of 5000 to 10000.").name)
    print(router("What payment methods do you accept?").name)
    print(router("Do you accept cash as a payment option?").name)
    print(router("How old are you?").name)