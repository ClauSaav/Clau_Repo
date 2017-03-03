from lxml import html
import requests

page = requests.get('https://www.beeva.com/en/')
tree = html.fromstring(page.content)

title = buyers = tree.xpath('//title/text()')
