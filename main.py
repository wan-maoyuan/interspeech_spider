from typing import List
from bs4 import BeautifulSoup
import struct

import requests, os


BASE_URL = "https://www.isca-speech.org/archive/interspeech_2022/"
INDEX_FILE = r"./index.html"
PDF_DIR = r"./pdf"


def save_index_page():
	if os.path.exists(INDEX_FILE):
		os.remove(INDEX_FILE)

	resp = requests.get(BASE_URL)
	with open(INDEX_FILE, "w", encoding="utf-8")as f:
		f.write(resp.text)
	
def get_html_from_file() -> str:
	with open(INDEX_FILE, "r", encoding="utf-8")as f:
		lines = f.readlines()
		content = "".join(lines)
		return content

def get_pdf_page_url(content: str) -> List[str]:
	pdfUrlList = []

	soup = BeautifulSoup(content, 'html.parser')
	cards = soup.find_all(name='div', attrs={"class":"w3-card w3-round w3-white w3-padding"})
	for card in cards:
		aList = card.div.find_all('a')
		for a in aList:
			pdfUrl = BASE_URL + a.get('href')
			pdfUrlList.append(pdfUrl)
	return pdfUrlList

def download_pdf_by_url(urlList: List[str]):
	if not os.path.exists(PDF_DIR):
		os.mkdir(PDF_DIR)

	for pdfUrl in urlList:
		resp = requests.get(pdfUrl)
		soup = BeautifulSoup(resp.text, 'html.parser')
		title = soup.find('h3').get_text()
		title = title.replace(":", "：")
		title = title.replace("?", "？")
		title = title.replace("/", "")
		
		div = soup.find(name='div', attrs={"class":"w3-container w3-card w3-padding-large w3-white"})
		pdfUrl = BASE_URL + div.a.get('href')
		if os.path.exists(PDF_DIR + "/" + title+".pdf"):
			continue

		pdfContent = requests.get(pdfUrl)

		with open(PDF_DIR + "/" + title+".pdf", "wb")as f:
			for x in pdfContent.content:
				a = struct.pack('B', x)
				f.write(a)


if __name__ == "__main__":
	save_index_page()
	content = get_html_from_file()
	urls = get_pdf_page_url(content)
	download_pdf_by_url(urls)

