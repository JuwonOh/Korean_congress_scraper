from .utils import get_soup
from .utils import now
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import re

## this function need to url from urls. use for
def parse_votting(url, picDeptCd):
    request_url = 'http://likms.assembly.go.kr/bill/memVoteResultDetailAjax.do'
    sessionCd = url.split('_')[1]
    currentsCd = url.split('_')[2]
    currentsDt = url.split('_')[3]
    picDeptCd = picDeptCd

    headers = {'Referer': url,'Accept-Language': 'ko-KR','host' : 'likms.assembly.go.kr','Origin': 'http://likms.assembly.go.kr','Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'ko-KR','Accept-Encoding':'gzip','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Referer': 'http://likms.assembly.go.kr/bill/memVoteDetail.do', 'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    data = {'sessionCd' :sessionCd, 'currentsCd': currentsCd, 'currentsDt': currentsDt, 'picDeptCd' :picDeptCd, 'pageSize': 200}


    response = requests.post(request_url, headers=headers,  data=data)
    decoded_text = response.content.decode("utf-8")
    text = temp.split('{"')[3:]
    json_list = [json.loads("{\"" + re.search('seq":\d(.+?)}', w).group(0)) for w in text]

def scrap_same_name(html_file):
    soup = BeautifulSoup(html_file)
    sub_links = kim1.find('div', class_= "subLnb2 subLnb2_1").find_all('a')
    sub_picDeptCd = kim1.find('div', class_= 'person')
    picDeptCd = int(re.findall('[0-9]{7}', str(sub_picDeptCd))[0])
    onclick = [i['onclick'] for i in sub_links]
    session_code = [re.sub("[^0-9,]","", w) for w in onclick]
    urls = [w.replace(',', '_') for w in session_code]
    json_list = []
    for url in urls:
        vote_result = parse_votting(url, picDeptCd)
        if not vote_result:
            continue
        json_list.extend(parse_votting(url, picDeptCd))
        result = pd.DataFrame(json_list)[['billNo', 'billKindCd', 'currCommittee', 'billName', 'procDt', 'procResultCd', 'resultVote']]
        file_name = '{}.xlsx'.format(html_file)
        result.to_excel(file_name)


def parse_table(bill_no, bill_id):
    request_url = 'http://watch.peoplepower21.org/opages/Lawinfo/_vote_table.php'
    url_base = 'http://watch.peoplepower21.org/?mid=LawInfo&bill_no={}'
    url = url_base.format(bill_no)

    data = {'term_no' :20, 'meetingbill_id': bill_id}

    headers = {'Referer': url,
               'Accept-Language': 'ko-KR',
                'host' : 'watch.peoplepower21.org',
                'Origin': 'http://watch.peoplepower21.org',
                'Accept-Encoding':'gzip',
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

    response = requests.post(request_url, headers=headers,  data=data)
    html = response.content
    page = BeautifulSoup(html, 'lxml')

    table = page.find_all('tr')
    element = [status.text for status in table]
    opts = ['반대','기권','불참', '출장','청가', '결석','찬성']
    ele_dic ={}

    for opt in opts:
        for ele in element:
            if opt in ele:
                words = re.findall('[\n]+[가-힣]{3}|[\n]+[가-힣]{2}', ele)
                names = [w.replace('\n', '') for w in words]
                ele_dic[opt] = [','.join(names[:len(names)])]
            else:
                continue
    return ele_dic

def parse_legislate(url):
    def parse_title(soup):
        title = soup.find('h1', align='center')
        if not title:
            return 'title error'
        return title.text

    def parse_commitee(soup):
        commitee = soup.find('div', class_='panel-body')
        if not commitee:
            return ' '
        return commitee.find('h4', align= 'center').text[11:]

    def parse_initiator(soup):
        initiator = soup.find_all('div', class_= 'panel-body')
        if not initiator[2]:
            return ' '
        return re.sub('\s+', ',', initiator[2].text)

    def parse_vote(soup):
        vote = soup.find('span', style= 'font-weight: 600')
        if not vote:
            return ' '
        return vote.text

    def parse_summury(soup):
        summury = soup.find('div', class_= 'textType02')
        if not summury:
            return 'summury_error'
        return summury.text

    def parse_js_id(soup):
        main = soup.find('div' , class_ = 'panel-group')
        if not main:
            return 'empty js script'
        js_str = main.find_all('script')
        if not js_str:
            return 'empty js script'
        js_id = re.findall('[0-9]{5}', js_str[1].text)
        return js_id[0]

    soup = get_soup(url)

    bill_id = url[52:]
    bill_no = parse_js_id(soup)

    fist_dic =  {
            'url': url,
            'title': parse_title(soup),
            'initiator': parse_initiator(soup),
            'commitee' :parse_commitee(soup),
            'vote_result' : parse_vote(soup),
            'summury': parse_summury(soup),
            'scraping_date': now()
    }

    if 'empty js script' in bill_no:
        return fist_dic
    else:
        fist_dic.update(parse_table(bill_id, bill_no))
        return fist_dic
