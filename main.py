import requests, time
from bs4 import BeautifulSoup as bs
import csv, os, time, re
#from download import download

header = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Cache-Control':'max-age=0'
}
green= "\033[0;32m"
blue= "\033[0;36m"
red= "\033[31;1m"

def pencarian():
    cari = input("\n\tMau cari anime apa: ")
    try: 
        url = "https://otakudesu.bid/?s={}&post_type=anime".format(cari)
        req = requests.get(url, headers=header)
        bes = bs(req.text, "html.parser")
    except IndexError:
        print("Ditulis ya ajg")
        os.system("clear")
        os.system("exit")
    return bes

def ongoing():
        url = ["https://otakudesu.bid/ongoing-anime","https://otakudesu.bid/ongoing-anime/page/2","https://otakudesu.bid/ongoing-anime/page/3"]
        res = [bs(requests.get(i,headers=header).text,'html.parser') for i in url]
        reslin = {}
        resld=[]
        resljdl = []
        for i in res:
        	for n,x in enumerate(i.findAll('div','thumb'),1):
        		resld.append(x.find("a",attrs={"data-wpel-link":"internal"})["href"])
        for i in res:
        	for n,x in enumerate(i.findAll("img","attachment-thumb size-thumb wp-post-image"),1):
        		resljdl.append(x["alt"])
        [print(n,i) for n,i in enumerate(resljdl,1)]
        pil = input("\n\tpilihh: ")
        pier = input("\n1.pereps\n2.batch\n1/2: ")
        if pier == "1":
            pereps(resld[int(pil)-1])
        elif pier == "2":
            execute(resld[int(pil)-1])
        
def milih():
    bs = pencarian()
    global resultpil
    name = bs.find("li", attrs={"style":"list-style:none;"})
    print("="*60)
    print("\n\t\t     ________________ \n\t\t    | Dipilih ya ajg |\n\t\t     ````````````````")
    result_judul = []
    result_link = []
    if name is None:
        print('Not found\n Ulangi nulis yg bener boss')
        exit()
    else:
        for i in bs.find_all('li', attrs={'style':'list-style:none;'}):
            result_judul.append(i.find("a", attrs={"data-wpel-link":"internal"}).string)
            result_link.append(i.find("a")["href"])
    [print(n,i) for n,i in enumerate(result_judul,1)]
    pilih = int(input("Pilih Nomerr brp: "))-1
    resultpil = result_link[pilih]
    pilb = input("\n1. pereps\n2. batch? \n1/2: ")
    #pilb = "1"
    print(resultpil)
    if pilb == "1":
        pereps(resultpil)
    elif pilb == "2":
        execute(resultpil)
    else:
        print("your input out of average")

global resul
resul = []

def pereps(url):
        resl = []
        rek = bs(requests.get(url,headers=header).text,"html.parser")
        for i in rek.findAll("a",attrs={"target":"_blank"}):
            lin = i["href"]
            if "-episode-" in lin or "-sp" in lin or "-spesial-" in lin:
                resl.append(i.string); resul.append(lin)
            else: pass  
        resul.reverse(); resl.reverse()
        os.system("clear")
        [print(n,i) for n,i in enumerate(resl,1)]
        if rek.find("div","sinopc").find("p").string is not None:
            print("\n",rek.find("div","sinopc").find("p").string,"\n")
        eps = resul
        rr = {}
        #try:
        pi = int(input("Pilih eps berapa? "))-1
        if "-episode-" in eps[pi] or "special" in eps[pi] or "-sp-" in eps[pi] or "ova" in eps[pi]:
            rek = bs(requests.get(eps[pi], headers=header).text, "html.parser").find("div","download")
            lili = rek.findAll("li")
            for n,i in enumerate(lili,1):
                rr[n]=i
                print(n)
            #mendownload resolusi default 480p.mkv
            res = [i for i in rr[2].find_all("a", attrs={"data-wpel-link":"external"})]
            lin = requests.get(res[0]["href"], headers=header)
            print(res[0]["href"])
            bes = bs(lin.text, "html.parser")
            origin = re.search('(.*?)/',bes.find("meta",attrs={"property":"og:url"})["content"].strip("/")).group(1)
            elemen = re.search('document.getElementById\(\'dlbutton\'\).href = \"(.*?)\" \+ \((.*?)\) \+ \"(.*?)\";',lin.text)
            print(bes.find("meta",attrs={"property":"og:url"})["content"].strip("/"))
            print("Please wait file downloading...\nFile size",bes.findAll("font",attrs={"style":"line-height:18px; font-size: 13px;"})[0].string)
            urldl = f"https://{origin}{elemen.group(1)}{eval(elemen.group(2))}{elemen.group(3)}"
            print(urldl)
            name = urldl.split("/")
            reks = requests.get(urldl,stream=True)
            with open(f"/sdcard/Download/video/{name[len(name)-1]}","wb") as fd:
                for chunk in reks.iter_content(chunk_size=1024*1024):
                    if chunk:
                        fd.write(chunk)
                fd.close()
                print("file",name[-1],"downloaded")
            
            """except Exception as ex:
            print(ex,ex.__traceback__.tb_lineno)
            print("owkw")"""
        
def execute(url):
    #link = milih()
    resl = []
    try:
        #pilih = int(input("Pilih Nomooor brp: "))-1
        os.system("clear")
        print("="*60)
        print("\n\t\t     ________________ \n\t\t    | Dipilih ya ajg |\n\t\t     ````````````````")
        rek = requests.get(url, headers=header)
        soup = bs(rek.text, "html.parser")
        print(url)
        for i in  soup.find_all("a",attrs={"target":"_blank"}):
            lin = i["href"]
            if "-episode-" in lin or "-sp" in lin or "-spesial-" in lin:
                resl.append(i.string); resul.append(lin)
            else:
                pass
        resul.reverse();resl.reverse()
        [print(n,i) for n,i in enumerate(resl,1)]
        main()
    except ValueError:
        print("Pilih nomor angka ya ajg\n")
        os.system("clear")
        os.system("exit")

def main():
    eps = resul
    rr = {}
    #kalo mau download batch ongoing
    #ganti try ke for i in range(len(eps)):
    #sama exceptnya ditutup
    #pilihan inputnya ditutup
    #try:
    for i in range(len(eps)):
        #pi = int(input("Piiilih Nomor brp: "))-1
        os.system("clear")
        print("="*50)
        """if "batch" in eps[pi] or "-batch-" in eps[pi]:
                rek = requests.get(eps[pi], headers=header)
                soup = bs(rek.text, "html.parser").find("div","batchlink")
                lili = soup.find_all("li")
                for n,i in enumerate(lili,1):
                    rr[n]=i
                    print(n,i.find("strong").string)"""
        #eps[pi] sama request.get(eps[pi]) diganti eps[i]
        if "-episode-" in eps[i] or "special" in eps[i] or "-sp-" in eps[i] or "ova" in eps[i]:
            rek = bs(requests.get(eps[i], headers=header).text, "html.parser").find("div","download")
            lili = rek.find_all("li")
            print(eps[i])
            #print("\n\tPilih resolusinya: ")
            for n,d in enumerate(lili,1):
                rr[n]=d
        #pil = int(input("\tpil: "))
        #disini ganti resolusinya print aja rr
        #rr[1:3] == 360p-480p.mp4
        #rr[4:6] == 480p.mkv
        res = [i for i in rr[2].find_all("a", attrs={"data-wpel-link":"external"})]
        lin = requests.get(res[0]["href"])
        bes = bs(lin.text,"html.parser")
        print(res[0]["href"])
        print(res[0].string)
        #.find("meta",attrs={"property":"og:url"})["content"].strip("/")
        origin = re.search('(.*?)/',bes.find("meta",attrs={"property":"og:url"})["content"].strip("/")).group(1)
        #print(bes.find("meta",attrs={"property":"og:url"})["content"].strip("/"))
        #origin = bs(lin.text,"html.parser").findAll("div","video-share")[0].find("input",attrs={"readonly":"readonly"})["value"]
        elemen = re.search('document.getElementById\(\'dlbutton\'\).href = \"(.*?)\" \+ \((.*?)\) \+ \"(.*?)\";',lin.text)
        print("Please wait file downloading...\nFile size",bes.findAll("font",attrs={"style":"line-height:18px; font-size: 13px;"})[0].string)
        urldl = f"https://{origin}{elemen.group(1)}{eval(elemen.group(2))}{elemen.group(3)}"
        print(urldl)
        name = urldl.split("/")
        r = requests.get(urldl,stream=True)
        folder = os.path.join("/sdcard/Download/video",name[-1][:18])
        file = os.path.join(folder,name[-1])
        if not os.path.exists(folder):
            os.makedirs(folder)
            fd = open(file,"wb")
            [fd.write(chunk) for chunk in r.iter_content(chunk_size=1024*1024) if chunk]
            fd.close()
        else:
            if not os.path.exists(file):
                fd = open(file,"wb")
                [fd.write(chunk) for chunk in r.iter_content(chunk_size=1024*1024) if chunk]
                fd.close()
            else:
                print("file is exists ",file,"\ncontinueing download")
                time.sleep(2)
        print("file",name[len(name)-1],"downloaded")
    """except ValueError:
        print("Pilihanya sampe 6 ya ajg")
        os.system("clear")
        os.system("exit")"""


def batcher():
    try:
        url = [bs(requests.get(f"https://otakudesu.bid/complete-anime/page/{i}/").text,"html.parser") for i in range(1,6)]
        n=1; reslink = []
        for i in url:
            for x,y in zip(i.findAll("div","thumb"), i.findAll("img","attachment-thumb size-thumb wp-post-image")):
                reslink.append(x.find("a",attrs={"data-wpel-link":"internal"})["href"])
                print(n,y["alt"]); n+=1
        pil = input("Pilih nomor: ")
        pilb = input("\n1. pereps\n2. batch? \n1/2: ")
        if pilb == "1":
            pereps(reslink[int(pil)-1])
            print(reslink[int(pil)-1])
        elif pilb == "2":
            execute(reslink[int(pil)-1])
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
        os.system("clear")
        print(blue+"   ____  __        __             __               \n  / __ \/ /_____ _/ /____  ______/ /__  _______  __\n / / / / __/ __ `/ //_/ / / / __  / _ \/ ___/ / / /\n/ /_/ / /_/ /_/ / ,< / /_/ / /_/ /  __(__  ) /_/ / \n\____/\__/\__,_/_/|_|\__,_/\__,_/\___/____/\__,_/  ")
        print(green+"   ____\n  / ___/______________ _____  ____  ___  _____\n  \__ \/ ___/ ___/ __ `/ __ \/ __ \/ _ \/ ___/\n ___/ / /__/ /  / /_/ / /_/ / /_/ /  __/ /    \n/____/\___/_/   \__,_/ .___/ .___/\___/_/     \n                    /_/   /_/                 ")
        stme = time.time()
        pil = input("\n\t1. Anime terkini OnGoing\n\t2. Cari anime\n\t3. Anime Batch selesai\n\t Pilih: ")
        #pil = "2"
        if pil == "1":
            ongoing()
        elif pil == "2":
            milih()
        elif pil == "3":
            batcher()
        else:
            print("Your input not in average")
        sce = time.time()-stme
        print("time taken", time.strftime("%H:%M:%S",time.gmtime(sce)))
