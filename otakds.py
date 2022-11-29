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

def milih():
    bs = pencarian()
    name = bs.find("li", attrs={"style":"list-style:none;"})
    print("="*60)
    print("\n\t\t     ________________ \n\t\t    | Dipilih ya ajg |\n\t\t     ````````````````")
    result_judul = []
    result_link = []
    if name is None:
        print('Not found')
    else:
        for i in bs.find_all('li', attrs={'style':'list-style:none;'}):
            result_judul.append(i.find("a", attrs={"data-wpel-link":"internal"}).string)
            result_link.append(i.find("a")["href"])
    [print(n,i) for n,i in enumerate(result_judul,1)]
    return result_link

def execute():
    link = milih()
    res = [];resl = []
    try:
        pilih = int(input("Pilih Nomor brp: "))-1
        os.system("clear")
        print("="*60)
        print("\n\t\t     ________________ \n\t\t    | Dipilih ya ajg |\n\t\t     ````````````````")
        rek = requests.get(link[pilih], headers=header)
        soup = bs(rek.text, "html.parser")
        for i in  soup.find_all("a",attrs={"target":"_blank"}):
            lin = i["href"]
            if "-episode-" in lin or "-sp" in lin or "-spesial-" in lin:
                resl.append(i.string); res.append(lin)
            else:
                pass
        res.reverse();resl.reverse()
        [print(n,i) for n,i in enumerate(resl,1)]
    except ValueError:
        print("Pilih nomor angka ya ajg\n")
        os.system("clear")
        os.system("exit")
    return res

def main():
    eps = execute()
    try:
        pi = int(input("Piiilih Nomor brp: "))-1
        os.system("clear")
        print("="*50)
        rr = {}
        """if "batch" in eps[pi] or "-batch-" in eps[pi]:
                rek = requests.get(eps[pi], headers=header)
                soup = bs(rek.text, "html.parser").find("div","batchlink")
                lili = soup.find_all("li")
                for n,i in enumerate(lili,1):
                    rr[n]=i
                    print(n,i.find("strong").string)"""
        if "-episode-" in eps[pi] or "special" in eps[pi] or "-sp-" in eps[pi] or "ova" in eps[pi]:
            rek = bs(requests.get(eps[pi], headers=header).text, "html.parser").find("div","download")
            lili = rek.find_all("li")
            print("\n\tPilih resolusinya: ")
            for n,i in enumerate(lili,1):
                rr[n]=i
                print("\t",+n,i.find("strong").string)
        pil = int(input("\tpil: "))
        res = [i for i in rr[pil].find_all("a", attrs={"data-wpel-link":"external"})]
        lin = requests.get(res[0]["href"])
        bes = bs(lin.text,"html.parser")
        #.find("meta",attrs={"property":"og:url"})["content"].strip("/")
        origin = re.search('(.*?)/',bes.find("meta",attrs={"property":"og:url"})["content"].strip("/")).group(1)
        #origin = bs(lin.text,"html.parser").findAll("div","video-share")[0].find("input",attrs={"readonly":"readonly"})["value"]
        elemen = re.search('document.getElementById\(\'dlbutton\'\).href = \"(.*?)\" \+ \((.*?)\) \+ \"(.*?)\";',lin.text)
        print(bes.find("meta",attrs={"property":"og:url"})["content"].strip("/"))
        print("Please wait file downloading...\nFile size",bes.findAll("font",attrs={"style":"line-height:18px; font-size: 13px;"})[0].string)
        urldl = f"https://{origin}{elemen.group(1)}{eval(elemen.group(2))}{elemen.group(3)}"
        print(urldl)
        name = urldl.split("/")
        reks = requests.get(urldl,stream=True)
        if os.path.exists("/sdcard/Download/video/"):
            with open(f"/sdcard/Download/video/{name[len(name)-1]}","wb") as fd:
                for chunk in reks.iter_content(chunk_size=1024*1024):
                    if chunk:
                        fd.write(chunk)
                fd.close()
            print("file",name[len(name)-1],"downloaded")
        else:
            with open(f"DownloadedAnime/{name[-1]}","wb") as fd:
                for chunk in reks.iter_content(chunk_size=1024*1024):
                    if chunk:
                        fd.write(chunk)
                fd.close()
            print("file",name[len(name)-1],"downloaded")
    except ValueError:
        print("Pilihanya sampe 6 ya ajg")
        os.system("clear")
        os.system("exit")
        
if __name__ == "__main__":
    os.system("clear")
    print(blue+"   ____  __        __             __               \n  / __ \/ /_____ _/ /____  ______/ /__  _______  __\n / / / / __/ __ `/ //_/ / / / __  / _ \/ ___/ / / /\n/ /_/ / /_/ /_/ / ,< / /_/ / /_/ /  __(__  ) /_/ / \n\____/\__/\__,_/_/|_|\__,_/\__,_/\___/____/\__,_/  ")
    print(green+"   ____\n  / ___/______________ _____  ____  ___  _____\n  \__ \/ ___/ ___/ __ `/ __ \/ __ \/ _ \/ ___/\n ___/ / /__/ /  / /_/ / /_/ / /_/ /  __/ /    \n/____/\___/_/   \__,_/ .___/ .___/\___/_/     \n                    /_/   /_/                 ")
    stme = time.time()
    main()
    sce = time.time()-stme
    print("time taken", time.strftime("%H:%M:%S",time.gmtime(sce)))
