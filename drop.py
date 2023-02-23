import requests
from bs4 import BeautifulSoup as bes

url = 'https://drop.download/7mb0ngh29zaa'
ses = requests.Session()
ses.headers = {
        "User-Agent":"Mozilla/5.0 (Linux; Android 11; M2010J19CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
        "Cache-Control":"max-age=0"
        }
r = ses.get(url).text
sop = bes(r,"html.parser")
"""for i in sop.findAll("div","form-row text-center"):
    print(i.findAll("div","col-6"))"""
code = sop.findAll("div",attrs={"class":"mb-4 mb-lg-6 d-flex justify-content-center"})
#width:80px;height:26px;font:bold 13px Arial;background:#ccc;text-align:left;direction:ltr;"})
print(code)
