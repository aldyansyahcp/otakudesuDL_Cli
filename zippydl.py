from zippyshare_downloader import extract_info, extract_info_coro

# by default, parameter download is True
def downloader(url,name,fol):
    file = extract_info(url, filename=name,download=True,folder=fol,replace=False)
    print(file)
    
#url = "https://www32.zippyshare.com/v/lVBY047m/file.html"
#url = "https://desudrive.com/link/?id=eVYzczJaUk9LU0lUMzFEYVlZam9XQkY1ajBwY25zVk9ZcWlIalJnZlkrdWZoRDcvWlpCcEtCd0k3OFZZdHNsWnpnPT0="
#downloader(url)
