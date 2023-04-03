"""Module for manipulating and generating PDFs"""
import requests
import json
from api2pdf import Api2Pdf

API2PDF_API_KEY = '36245866-5ad3-4d48-8911-31b9d9f84966' # get key from portal.api2pdf.com/register
USERAGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def make_pdf_from_url(url, options=None):
    """Produces a pdf from a website's url.
    Args:
        url (str): A valid url
        options (dict, optional): for specifying pdf parameters like landscape
            mode and margins
    Returns:
        pdf of the website
    """
    a2p_client = Api2Pdf(API2PDF_API_KEY)
    pdf_response = a2p_client.HeadlessChrome.convert_from_url(url, options=options)
    if pdf_response['success']:
        download_response = requests.get(pdf_response['pdf'], headers=USERAGENT)
        data = download_response.content
        return data
    else:
        return None

def make_pdf_from_raw_html(html, options=None):
    """Produces a pdf from raw html.
    Args:
        html (str): Valid html
        options (dict, optional): for specifying pdf parameters like landscape
            mode and margins
    Returns:
        pdf of the supplied html
    """
    a2p_client = Api2Pdf(API2PDF_API_KEY)
    pdf_response = a2p_client.HeadlessChrome.convert_from_html(html, options=options)
    if pdf_response['success']:
        download_response = requests.get(pdf_response['pdf'], headers=USERAGENT)
        data = download_response.content
        return data
    else:
        return None


make_pdf_from_url('https://elearning.msu.ac.zw/login', options=None)