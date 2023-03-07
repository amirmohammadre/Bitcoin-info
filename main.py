from flask import Flask, render_template
import requests
from time import time
from lxml import etree
from bs4 import BeautifulSoup



app = Flask(__name__)


url = "https://explorer.btc.com/btc"

Dict_Headers = ({'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
    'Accept-Language': 'en-US, en;q=0.5'})

webPage = requests.get(url,Dict_Headers)
Scraping = BeautifulSoup(webPage.content, "html.parser") 

documentObjectModel = etree.HTML(str(Scraping)) 

height       = documentObjectModel.xpath('//*[@id="__next"]/div[1]/div/div[5]/div/div[3]/div/table/tbody/tr[1]/td[1]/a')[0].text
mined_by	 = documentObjectModel.xpath('//*[@id="__next"]/div[1]/div/div[5]/div/div[3]/div/table/tbody/tr[1]/td[2]/div/a/span')[0].text
time_mined	 = documentObjectModel.xpath('//*[@id="__next"]/div[1]/div/div[5]/div/div[3]/div/table/tbody/tr[1]/td[3]/div')[0].text
reward	     = documentObjectModel.xpath('//*[@id="__next"]/div[1]/div/div[5]/div/div[3]/div/table/tbody/tr[1]/td[4]/div')[0].text

#------------------------------------------------------------------

tx_hash  = documentObjectModel.xpath('//*[@id="__next"]/div[1]/div/div[6]/div/div[3]/div/table/tbody/tr[1]/td[1]/div/a')[0].text
time_trx = documentObjectModel.xpath('//*[@id="__next"]/div[1]/div/div[6]/div/div[3]/div/table/tbody/tr[1]/td[2]/div')[0].text
amount   = documentObjectModel.xpath('//*[@id="__next"]/div[1]/div/div[6]/div/div[3]/div/table/tbody/tr[1]/td[3]/div')[0].text



###################################################################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats')
def stats():
    return render_template('stats.html', ht = height, md = mined_by
                            , tm_md = time_mined, rw = reward)

@app.route('/trxs')
def trxs():
    return render_template('trxs.html', th = tx_hash, tm_tx = time_trx
                            , amt = amount)



if __name__ == '__main__':
    app.run(debug=True)