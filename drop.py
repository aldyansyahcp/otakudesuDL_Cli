import requests, pixeldrain, wget, os, time
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from pykraken.kraken import Kraken
#from main import resdulu

ses = requests.Session()
ses.headers = {
        "User-Agent":"Mozilla/5.0 (Linux; Android 11; M2010J19CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
        "Cache-Control":"max-age=0"
        }
krk = Kraken()

def dlpers(url):
    global reslin
    reslin = []
    resdul = []
    rek = bs(ses.get(url).text,"html.parser")
    for i in rek.findAll("a",attrs={"target":"_blank"}):
        lin = i["href"]
        if "-episode-" in lin or "-sp" in lin or "-spesial-" in lin:
            reslin.append(lin); resdul.append(i.string)
        else: pass
    reslin.reverse(); resdul.reverse()
    #os.system("clear")
    [print(n,i) for n,i in enumerate(resdul,1)]
    if rek.find("div","sinopc").find("p") is not None:
        print("\n",rek.find("div","sinopc").find("p").text,"\n")
    else: pass
    eps = reslin
    linkeps = {}
    linkepsb = {}
    pil = int(input("Pilih eps brp/Kalau batch tulis 99: "))-1
    finalink = []
    finalinkb = []
    try:
        if pil == 98:
            dlbatch()
            """print("batch bang")
            for i in reslin:
                req = bs(ses.post(i).text,"html.parser")
                judul = req.find("h1","posttl").text.replace(" ","")+".mkv"
                dlp = req.find("div","download")
                lili = dlp.findAll("li")
                for n,i in enumerate(lili,1):
                    linkepsb[n]=i
                    #print(i.find("strong").text,i.find("a").text)
                for i in linkepsb[3].findAll("a"):
                    if "Pdrain" in i.text:
                        finalinkb.append(i["href"])
                        if len(finalinkb) == 0:
                            print("Pixeldrain not found")
                        else:
                            rurl = ses.post(i["href"]).url.split("/")[-1]
                            down = "https://pixeldrain.com/api/file/"+rurl
                            names = pixeldrain.info(str(rurl))["name"]
                            #outp = wget.download(down)
                            print(names)
                            folder = os.path.join("/sdcard/Download/video", judul.replace(" ","")[0:8])
                            file = os.path.join(folder,names)
                            if not os.path.exists(folder):
                                os.makedirs(folder)
                                wget.download(down,out=folder)
                            else:
                                if os.path.exists(names):
                                    print("File exists\n\t CONTINUEING DOWNLOAD BATCH")
                                    time.sleep(3)
                                else:
                                    wget.download(down,out=folder)
                    else: pass"""
        else:
            req = bs(ses.post(reslin[pil]).text,"html.parser").find("div","download")
            lili = req.findAll("li")
            for n,i in enumerate(lili,1):
                linkeps[n]=i
                print(i.find("strong").string,i.find("a").text)
                #print(i.findAll("a").text)#check pixeldrainya ada ga
                #RESOLUSI DISINI BANH ini otomatis mkv 480p
            #sementara bisa buatnya pixeldrain downloader doang 
            for i in linkeps[3].findAll("a"):
                print(i.text)
                if "Pdrain" in i.text:
                    finalink.append(i["href"])
                    if len(finalink) == 0:
                        print("pixeldrain not found")
                    else:
                        rurl = ses.post(i["href"]).url.split("/")[-1]
                        down = "https://pixeldrain.com/api/file/"+rurl
                        #size = int(down.headers.get("content-lenght",1))
                        wget.download(down,out="/sdcard/Download/video")               
                else:
                    if "Kraken" in i.text:
                        finalink.append((i["href"]))
                        if len(finalink) == 0:
                            print("Krakendl not found")
                        else:
                            rurl = ses.post(i["href"])
                            down = krk.get_download_link(rurl)
                            names = bs(rurl.text,"html.parser").find("h5").string
                            file = os.path.join(file,folder)
                            reks = ses.get(down,stream=True)
                            with open(file, "wb") as fd:
                                for chunk in tqdm(reks.iter_content(1024*1024)):
                                    if chunk:
                                        fd.write(chunk)
                                fd.close()
                            #print(down)
                            #wget.download(down,out="/sdcard/Download/video")
                else:
                    print("Pixeldrain Or Krakenfiles downloader not found")
    except IndexError:
        print("Your index out of range")
        
def dlbatch():
            linkepsb = {}
            finalinkb = []
            print("batch bang")
            for i in reslin:
                req = bs(ses.post(i).text,"html.parser")
                judul = req.find("h1","posttl").text.replace(" ","")+".mkv"
                folder = os.path.join("/sdcard/Download/video", judul.replace(" ","")[0:8])
                dlp = req.find("div","download")
                lili = dlp.findAll("li")
                for n,i in enumerate(lili,1):
                    linkepsb[n]=i
                    #print(i.find("strong").text,i.find("a").text)
                for i in linkepsb[3].findAll("a"):
                    if "Pdrain" in i.text:
                        finalinkb.append(i["href"])
                        if len(finalinkb) == 0:
                            print("Pixeldrain not found")
                        else:
                            rurl = ses.post(i["href"]).url.split("/")[-1]
                            down = "https://pixeldrain.com/api/file/"+rurl
                            names = pixeldrain.info(str(rurl))["name"]
                            #outp = wget.download(down)
                            file = os.path.join(folder,names)
                            if not os.path.exists(folder):
                                os.makedirs(folder)
                                wget.download(down,out=folder)
                            else:
                                if os.path.exists(names):
                                    print("File exists\n\t CONTINUEING DOWNLOAD BATCH")
                                    time.sleep(3)
                                else:
                                    wget.download(down,out=folder)
                    else:
                        if "Kraken" in i.text:
                            finalinkb.append(i["href"])
                            if len(finalinkb) == 0:
                                print("Krakendl notfound")
                            else:
                                rurl = ses.post(i["href"])
                                down = krk.get_download_link(rurl.url)
                                names = bs(rurl.text,"html.parser").find("h5").string
                                file = os.path.join(folder,names)
                                reks = ses.get(down,stream=True)
                                if not os.path.exists(folder):
                                    os.makedirs(folder)
                                    with open(file, "wb") as fd:
                                        for chunk in tqdm(reks.iter_content(chunk_size=1024*1024)):
                                            if chunk:
                                                fd.write(chunk)
                                        fd.close()
                                else:
                                    if not os.path.exists(file):
                                        with open(file,'wb') as fd:
                                            for chunk in tqdm(reks.iter_content(chunk_size=1024*1024)):
                                                if chunk:
                                                    fd.write(chunk)
                                            fd.close()
                    else:
                        print("Pixeldrain Or Krakenfiles url downloader not found")
                                    

"""        
url = "https://otakudesu.lol/anime/kanojo-koushaku-riyu-sub-indo/"    
#dlpers('https://otakudesu.lol/anime/oshi-noko-sub-indo/')
dlpers(url)
"""
