from sdk.python.sentiment_sdk import analyze_sentiment

# Test text sentiment
result = analyze_sentiment("I absolutely love this project!", mode="text")
print("Text Result:", result)