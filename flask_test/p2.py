from flask import Flask, send_file, render_template,request
import io 
import matplotlib.pyplot as plt 
import seaborn as sns
import snscrape.modules.twitter as sntwitter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
obj = SentimentIntensityAnalyzer()
import pickle
import json
import plotly
import plotly.express as px
import requests 
import os


fig,ax=plt.subplots(1,1)
positive=[]
negative=[]
compound1 = []
compound2 = []
likes=[]
tweetss = [] 
category=[]

limit = 2
limit2 = 2


cate=['category']
column=['Negative','Positve']
weeks=['Date','Sentiment']
likes2=['Tweet','Likes','Retweets']

def calculate_average(list):
    return sum(list) / len(list)  



with open('model.pkl', 'rb') as f:
            clf2 = pickle.load(f)

v= {6: 'CRIME', 10: 'ENTERTAINMENT', 39: 'WORLD NEWS', 18: 'IMPACT', 24: 'POLITICS', 36: 'WEIRD NEWS', 2: 'BLACK VOICES', 38: 'WOMEN', 5: 'COMEDY', 25: 'QUEER VOICES', 28: 'SPORTS', 3: 'BUSINESS', 34: 'TRAVEL', 20: 'MEDIA', 32: 'TECH', 26: 'RELIGION', 27: 'SCIENCE', 19: 'LATINO VOICES', 9: 'EDUCATION', 4: 'COLLEGE', 23: 'PARENTS', 1: 'ARTS & CULTURE', 29: 'STYLE', 15: 'GREEN', 31: 'TASTE', 16: 'HEALTHY LIVING', 33: 'THE WORLDPOST', 14: 'GOOD NEWS', 40: 'WORLDPOST', 12: 'FIFTY', 0: 'ARTS', 37: 'WELLNESS', 22: 'PARENTING', 17: 'HOME & LIVING', 30: 'STYLE & BEAUTY', 8: 'DIVORCE', 35: 'WEDDINGS', 13: 'FOOD & DRINK', 21: 'MONEY', 11: 'ENVIRONMENT', 7: 'CULTURE & ARTS'}


def get_tweets(query): 

    fetched_tweets = sntwitter.TwitterSearchScraper(query+" lang:en min_faves:50").get_items()
    tweets = [] 
    for tweet in fetched_tweets:
        if len(tweets) == limit:
            break
        else:     
            parsed_tweet = {} 
            parsed_tweet['text'] = tweet.content
            sentiment_dict = obj.polarity_scores(tweet.content)
            parsed_tweet['sentiment'] = sentiment_dict['compound'] 

            predicted = clf2.predict(tuple([tweet.content]))
            try: 
                a=v[predicted[0]]
            except:
                a='OTHER'    
            category.append([a])
            positive.append(sentiment_dict['pos'])
            negative.append(sentiment_dict['neg'])
            compound1.append(sentiment_dict['compound'])
            tweets.append(parsed_tweet) 
            likes.append([tweet.content,tweet.likeCount,tweet.retweetCount])
    return tweets 



def get_tweetss(query): 

    

    for tweet in sntwitter.TwitterSearchScraper(query+" min_faves:50 lang:en until:2022-12-24 since:2022-12-18 -filter:links -filter:replies").get_items():
        if len(tweetss) == limit2:
            break
        else:
            sentiment_dict = obj.polarity_scores(tweet.content)
            compound2.append(sentiment_dict['compound'])
            tweetss.append([tweet.date.strftime("%d/%m/%Y"),sentiment_dict['compound']])
            

            
            
app=Flask(__name__)


pic_folder=os.path.join('static','emojies')

app.config['UPLOAD_FOLDER']= pic_folder

@app.route ('/')
def home () :
    cities = ['Bangalore', 'Gurugram', 'Chandigarh', 'Hyderabad','Kolkata']
    return render_template('index.html', cities=cities)



@app.route("/predict", methods=['POST','GET'])
def pred():
	if request.method=='POST':
        
            query=request.form['query']
            city_name=request.form['query']
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=46d978f91cb52cddcafdc43b6a42f57c'
            
            response = requests.get(url.format(city_name.title())).json()
            try:
                temp = response['main']['temp']
                weather = response['weather'][0]['description']
                icon = response['weather'][0]['icon']
            except KeyError:
                temp = '0'
                weather = '0'
                icon = None
            
            fetched_tweets = get_tweets(query) 
            average = calculate_average(compound1)

            if average > 0.075:
                average =" Extremely positive"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'1.png')

            elif average > 0.050:
                average ="Significantly positive"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'2.png')

            elif average > 0.030:
                average ="Fairly positive"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'3.png')

            elif average > 0.010:
                average ="Slightly positive"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'4.png')

            elif average < -0.010:
                average ="Slightly negative"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'5.png')

            elif average < -0.030:
                average ="Fairly negative"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'6.png')

            elif average < -0.050:
                average ="Significantly negative"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'7.png')
            elif average < -0.075:
                average ="Extremely negative"
                pic=os.path.join(app.config['UPLOAD_FOLDER'],'8.png')


            get_tweetss(query)  
            
            df = pd.DataFrame(category, columns=cate)
            cat = df['category'].value_counts().rename_axis('category').reset_index(name='counts').head(5)
            df1 = pd.DataFrame(tweetss, columns=weeks)

            if(((request.form['query'])=='bangalore') or (request.form['query']=='Bangalore')):
                csv = pd.read_csv('bangalore1.csv')
                csv['Time'] = csv['Time'].str[:-10]
                avg = csv['Analysis'].mean()
                avg=round(avg,3)
                avg=avg*10

                fig = px.bar(csv ,x='Time',y='Analysis')

                csv2 = pd.read_csv('bangalore.csv')
                csv2['Time'] = csv2['Time'].str[:-10]
                avg2 = csv2['Analysis'].mean()
                avg2=avg2*10
                avg2=round(avg2,3)
                pic2=os.path.join(app.config['UPLOAD_FOLDER'],'bangalore.svg')

            elif(((request.form['query'])=='chandigarh') or (request.form['query']=='Chandigarh')):
                csv = pd.read_csv('chandigarh1.csv')
                csv['Time'] = csv['Time'].str[:-10]
                avg = csv['Analysis'].mean()
                avg=round(avg,3)
                fig = px.bar(csv ,x='Time',y='Analysis')

                csv2 = pd.read_csv('chandigarh.csv')
                csv2['Time'] = csv2['Time'].str[:-10]
                avg2 = csv2['Analysis'].mean()
                avg2=avg2*10
                avg2=round(avg2,3)
                pic2=os.path.join(app.config['UPLOAD_FOLDER'],'chandigarh.svg')
            

            elif(((request.form['query'])=='gurugram') or (request.form['query']=='Gurugram')):
                csv = pd.read_csv('gurugram1.csv')
                csv['Time'] = csv['Time'].str[:-10]
                avg = csv['Analysis'].mean()
                avg=round(avg,3)
                fig = px.bar(csv ,x='Time',y='Analysis')

                csv2 = pd.read_csv('gurugram.csv')
                csv2['Time'] = csv2['Time'].str[:-10]
                avg2 = csv2['Analysis'].mean()
                avg2=avg2*10
                avg2=round(avg2,3)
                pic2=os.path.join(app.config['UPLOAD_FOLDER'],'gurugram.svg')
                fig = px.bar(csv ,x='Time',y='Analysis')

            elif(((request.form['query'])=='hyderabad') or (request.form['query']=='Hyderabad')):
                csv = pd.read_csv('hyderabad1.csv')
                csv['Time'] = csv['Time'].str[:-10]
                avg = csv['Analysis'].mean()
                avg=round(avg,3)
                fig = px.bar(csv ,x='Time',y='Analysis')

                csv2 = pd.read_csv('hyderabad.csv')
                csv2['Time'] = csv2['Time'].str[:-10]
                avg2 = csv2['Analysis'].mean()
                avg2=avg2*10
                avg2=round(avg2,3)
                pic2=os.path.join(app.config['UPLOAD_FOLDER'],'hyderabad.svg')

            elif(((request.form['query'])=='kolkata') or (request.form['query']=='Kolkata')):
                csv = pd.read_csv('kolkata1.csv')
                csv['Time'] = csv['Time'].str[:-10]
                avg = csv['Analysis'].mean()
                avg=round(avg,3)
                fig = px.bar(csv ,x='Time',y='Analysis')

                csv2 = pd.read_csv('kolkata.csv')
                csv2['Time'] = csv2['Time'].str[:-10]
                avg2 = csv2['Analysis'].mean()
                avg2=avg2*10
                avg2=round(avg2,3)
                pic2=os.path.join(app.config['UPLOAD_FOLDER'],'kolkata.svg')

            else:
                avg=calculate_average(compound2)
                avg=round(avg,3)
                avg2=0
                fig = px.bar(df1, x='Date', y='Sentiment')
                pic2=os.path.join(app.config['UPLOAD_FOLDER'],'')

            avg1=calculate_average(compound1)
            avg1=round(avg1,3)

            if(avg1>avg):
                compare="Today's Analysis is better when compared with last week's"
            else:
                compare="Today's Analysis is worse when compared with last week's"


            if(avg2==0):
                compare2="No data found!!"
            elif(avg1>avg2):
                compare2="Today's Score is better when compared with Yearly Score"
            else:
                compare2="Today's Score is worse when compared with Yearly Score"
            

        
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            lk = pd.DataFrame(likes, columns=likes2)
            k=lk.max()

            t=k['Tweet']
            l=k['Likes']
            r=k['Retweets']

            compound1.clear()
            compound2.clear()
            likes.clear()
            tweetss.clear()
            category.clear()
            cities = ['Bangalore', 'Gurugram', 'Chandigarh', 'Hyderabad','Kolkata']

            return render_template('index.html',average=average,compare=compare,compare2=compare2,avg=avg,avg1=avg1,avg2=avg2, pic=pic,pic2=pic2, result=fetched_tweets,temp=temp,weather=weather,icon=icon, city_name = city_name, tables=[cat.to_html(index=False)],graphJSON=graphJSON,t=t,l=l,r=r,cities=cities)



    
@app.route("/visualize")
def visualize():
    pos = calculate_average(positive)
    neg = calculate_average(negative)
    labels= ['Postive', 'Negative']
    colors=['green', 'red']
    sizes= [pos, neg]
    plt.pie(sizes,labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    img=io.BytesIO()
    fig.savefig(img,transparent=True)
    img.seek(0)
    plt.clf()
    return send_file(img,mimetype='img/png')



if __name__ =="__main__":
    app.run(debug=True)