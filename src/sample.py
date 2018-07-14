from gensim.models import word2vec
from natto import MeCab
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import twitter

# 取得したキーとアクセストークンを設定する
auth = twitter.OAuth(consumer_key="GXhiiOmWD9i2hTLmbs5gARwyL",
                     consumer_secret="Rx2RzilANDV3IkFmILPWGW1DPDW9Hk4Bk6JxLnISKmLKPKu77B",
                     token="779635102988939264-oZIWz8kVzcCzwgsgwWZxnbEoH80iMDm",
                     token_secret="sgoXKK4fhL5iFfkNON3gKSdglwb9KpcuqTDjYZkOzYHb7")

t = twitter.Twitter(auth=auth)
text = ""

queries = ["プログラミング", "programming", "python"]

for query in queries:
    search = t.search.tweets(q = query, lang="ja", count=100)
    for tweet in search['statuses']:
        text  += tweet['text']

word_list = []

with MeCab('-F%m,%f[0],%h') as nm:
    for n in nm.parse(text, as_nodes=True):
        node = n.feature.split(',')
        if len(node) != 3:
            continue
        if node[1] == "名詞":
            if len(node[0]) > 1:
                word_list.append(node[0])
print(word_list)

model = word2vec.Word2Vec([word_list], size=1000, min_count=10, window=5, iter=100)
results = model.wv.most_similar(positive=['python'])
for result in results:
    print(result)
