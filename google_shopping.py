import re
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup


def search(product):
    root = 'https://www.google.com/search?q='
    suffix = '&tbm=shop'
    headers = {'User agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);'}

    link = root + re.sub('\s', '+', product) + suffix
    resp = requests.get(link, headers=headers).content

    if resp is not None:
        st.info('Sucesso na requisição')
    else:
        st.info('deu errado')
    return resp


def get_products(html):
    soup = BeautifulSoup(html, 'html.parser')

    st.write(soup)

    divs_com_preco = [
        i for i in 
        soup.findAll('div')
        if len(i.findAll('div')) >= 6
        if len([
            j for j in i.findAll('div')
            if 'R$' in str(j)
        ]) > 0
        and len([
            j for j in i.findAll('div')
            if 'de R$' in str(j)
        ]) == 0
    ]

    st.write(len(divs_com_preco))
    cols = [
        'site', 'titulo', 'preco', 'rating', 'imagem'
    ]
    produtos = pd.DataFrame(
        columns = cols
    )

    for div in divs_com_preco:
        vetor = []
        for a in div.findAll('a'):
            if len(a.findAll()) == 0:
                # site
                vetor.append(re.findall('https?://[^\/]+', str(a['href']))[0])
            if 'aria-hidden' not in a.attrs.keys() and len(a.findAll('span')) == 0:
                # titulo
                vetor.append(a.text)
        for span in div.findAll('span'):
            if 'R$' in span.text:
                # preco
                vetor.append(
                    float(
                        re.sub(',', '.', 
                            re.sub('\.', '', 
                                ''.join(
                                    re.findall('[0123456789\.,]', span.text)
                                )
                            )
                        )
                    )
                )
        # rating
        rating = div.text.count('★')
        if rating == 0:
            rating = None
        vetor.append(rating)
        for img in div.findAll('img'):
            # imagem
            vetor.append(str(img['src']))
        
        vetor_df = pd.DataFrame(vetor).T
        vetor_df.columns = cols
        produtos = produtos.append(vetor_df, ignore_index=True)
        st.write(produtos)
    return produtos
