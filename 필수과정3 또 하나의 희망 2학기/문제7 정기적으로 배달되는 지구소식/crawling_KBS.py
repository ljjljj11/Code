import requests
from bs4 import BeautifulSoup


def scrape_news():
    """KBS 뉴스 메인 페이지에서 주요 기사 제목을 추출한다."""
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'
    response = requests.get(url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    print('📢 KBS 뉴스 헤드라인\n')

    headlines = []

    for item in soup.select('div.box-contents p.title'):
        text = item.get_text(strip=True)
        if text and text not in headlines:
            headlines.append(text)

    return headlines


def scrape_stock():
    """네이버 금융에서 주요 지수 및 개별 종목 주가를 가져온다."""
    headers = {'User-Agent': 'Mozilla/5.0'}

    print('\n💹 주식 시장 요약\n')

    stock_info = {}

    # 주요 지수 (KOSPI, KOSDAQ, 환율)
    url_index = 'https://finance.naver.com/sise/'
    res_index = requests.get(url_index, headers=headers)
    res_index.encoding = 'euc-kr'
    soup_index = BeautifulSoup(res_index.text, 'html.parser')

    labels = ['KOSPI', 'KOSDAQ', 'USD/KRW']
    for a_tag in soup_index.find_all('a'):
        if a_tag.string and a_tag.string.strip() in labels:
            label = a_tag.string.strip()
            row = a_tag.find_parent('tr')
            if row:
                number_cell = row.select_one('td.number')
                if number_cell:
                    stock_info[label] = number_cell.get_text(strip=True)

    # 개별 종목 주가
    stock_codes = {
        '삼성전자': '005930',
        'SK하이닉스': '000660',
        'NAVER': '035420',
        '현대차': '005380',
        '카카오': '035720'
    }

    for name, code in stock_codes.items():
        url = f'https://finance.naver.com/item/main.nhn?code={code}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        price_tag = soup.select_one('p.no_today span.blind')
        if price_tag:
            stock_info[name] = price_tag.get_text(strip=True)

    return stock_info


def main():
    # 뉴스 출력
    news_list = scrape_news()
    for idx, headline in enumerate(news_list, start=1):
        print(f'{idx}. {headline}')

    # 주식 정보 출력
    stock_data = scrape_stock()
    print()
    for key, value in stock_data.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()
