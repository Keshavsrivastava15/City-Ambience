# City-Ambience


In our project, we are monitoring the city ambiance by capturing XML RSS feeds of distinct cities from different sources like Hindustan Times, Times of India, The Hindu, etc. The data that we capture is stored in our MySQL database which has been automated, i.e. it fetches the data automatically from all the sources in order to capture the data every day, and then sentiment analysis is performed on it using the VADAR sentiment analysis package which gives rating as positive, negative, neutral and compound. There are different parameters on which monitoring would be done. The data is also captured from Twitter using Twitter API and Tweeny. Comparative analysis of XML RSS feeds and Twitter data is also executed.
