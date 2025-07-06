import re

with open("wikipedia_article.html", "r", encoding="utf-8") as file:
    html_article = file.read()

print(html_article)

splitting_by = r"(?=<h1|<h2|<h3|</p><p|<ul|<table)"

chunks = re.split(splitting_by, html_article)

document_parts = []

for i, chunk in enumerate(chunks):
    print(i)
    print(chunk)
    document_parts.append(chunk)

print(document_parts)