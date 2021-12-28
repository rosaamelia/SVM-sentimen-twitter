import tweepy
import csv #Import csv
consumer_key =''
consumer_secret = ''
acces_token =''
acces_secret =''
auth = tweepy.OAuthHandler (consumer_key, consumer_secret)
auth.set_access_token(acces_token, acces_secret)
api = tweepy.API(auth)

# Open/create a file to append data to
csvFile = open('result4.csv', 'a',encoding='utf-8')

#Use csv writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,
                           q = "daring",
                           since = "2021-01-01",
                           until = "2021-05-24",
                           lang = "id").items(500):
    # Write a row to the CSV file. I use encode UTF-8
    csvWriter.writerow([tweet.created_at, tweet.text])
    print(tweet.created_at, tweet.text)
csvFile.close()