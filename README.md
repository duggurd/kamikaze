# Kamikaze

Stock strategy explained

Kamikaze live update and opportunities

Previous opportunities

What? Why? How?

## What is kamikaze?

A kamikaze is a stock that has recently dropped unexpectedly in value, and usually with alot of media and or social media coverage. This is usually a large cap companuy caucht up in a scandal or similar. The observation is that large movements in large companies usually stabilize and gain on the stock market.

The exception to the rule are companies that are actually struggling underneath and are on the road to bankruptcy.

Large cap companies usually have the resources and other means to redevelop and make necessary changes to become more attractive again to investors.

# TODO

- [ ] Fetch new stories from relevant sites
- [ ] Fetch social media posts
- [ ] Extract tickers
- [ ] Sentiment analysis
- [ ] Store data
- [ ] Website
- [ ] +++

# Requirements

- The solution shall have a easy user interface, that can be shared online, website
- The solution shall have one or more databases were data is stored and easily accessible to the website and to the backend
- The soltion shall rely on machine learning
- The solution shall use web scraping to gather text data from social media and other media
- The machine learning model should take a text input and output a sentiment ranging from very negative to very positive
- The website shall display potential inferred kamikaze opportunities
- The website shall display the current kamikaze outlook of large cap stocks

# Resources

Model: https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis

Serve: https://github.com/pytorch/serve/blob/master/examples/text_classification_with_scriptable_tokenizer/README.md

Vocab: https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis/raw/main/vocab.json
