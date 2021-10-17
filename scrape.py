import os
import requests
import typing

def download(url: str, filename: str) -> None:
    '''Download the website at *url* and save it to *filename*'''
    try:
        r = requests.get(url)
        with open(filename, 'w') as f:
            f.write(r.text)
    except:
        print ("Error trying to download " + url + ". Aborting.")
        raise SystemExit

    size = os.path.getsize(filename)
    if size > 0:
        print ("Downloaded " + str(size) + " bytes.")
    else:
        print ("Download failed. Aborting.")
        raise SystemExit


def main():
    # First set of chapters
    base_url = "https://www.projekt-gutenberg.org/goethe/brschil1/chap0"
    suffix = ".html"
    for nb in range(1,6):
        url = base_url + str(nb) + suffix
        filename = "./raw/" + str(nb) + ".html"
        download(url, filename)

    # Second set of chapters
    base_url = "https://www.projekt-gutenberg.org/goethe/brschil2/chap00"
    suffix = ".html"
    for nb in range(1,9):
        url = base_url + str(nb) + suffix
        filename = "./raw/" + str(nb+5) + ".html"
        download(url, filename)

if __name__ == "__main__":
    main()
