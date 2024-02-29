# City-Ambience

In my project, I'm monitoring the city ambiance by capturing XML RSS feeds of distinct cities from different sources like Hindustan Times, Times of India, The Hindu, etc. The data that I capture is stored in my MySQL database, which has been automated. It fetches the data automatically from all the sources every day. Afterward, I perform sentiment analysis on it using the VADAR sentiment analysis package, which provides ratings as positive, negative, neutral, and compound.

There are various parameters on which I conduct monitoring. Additionally, I capture data from Twitter using the Twitter API and Tweeny. I also execute comparative analysis of XML RSS feeds and Twitter data to gain deeper insights into the city ambiance.
