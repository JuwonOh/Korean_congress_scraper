# Korean_congress_scraper

20대 국회의원들의 개인 표결 기록을 수집하기 위한 크롤러입니다. 의원 개인의 인적정보와 소속정당과 법안 표결, 표결 내용를 수집합니다.

## Data source

korean_congress_scraper는 세가지 사이트에서 데이터를 수집합니다. 
의원 개인의 인적정보에 대한 데이터를 공공데이터 포털의 의원정보 api(https://www.data.go.kr/dataset/15012647/openapi.do)에서 제공하는 자료를 사용합니다.
의회에서 이뤄지는 법안에 대한 표결 정보는 2가지 사이트에서 수집합니다. 
먼저 참여연대 열려라 국회(http://watch.peoplepower21.org/index.php)에서 제공하는 법안 정보를 수집합니다.
하지만 열려라 국회는 동명이인을 구별하지 않기때문에, 보조적으로 국회 의안정보 시스템(http://likms.assembly.go.kr/bill/main.do)를 사용해서, 이름이 동일한 의원들의 표결기록을 수집했습니다.

## Usage

scraper의 searching_a_query.py를 통해 참여연대 열려라 국회에서 제공하는 의원의 표결자료를 수집할 수 있습니다. 
searching_a_query.py에서 지정 할 수 있는 조건은 4가지입니다. 
bill_result는 법안의 결과를 기준으로 표결결과를 수집합니다. "부결", "원안가결", "수정가결", "철회"가 가능합니다. 
max_page는 수집할 법안의 수를 지정할 수 있습니다. 
begin_date에는 원하는 기간의 첫날을, end_date에는 원하는 기간의 마지막 날을 적으면 됩니다.
예를 들어 searching_a_query.py --bill_result "원안가결" --max_page "10" --begin_date "2017-01-01" -- end_date "2018-01-01"을 지정하면, 2017년 1월 1일부터 2018년 1월 1일까지 원안가결된 법안이 10000개의 표결기록을 수집합니다.


## Folder Structure
  ```
  Korean_congress_scraper/
  │
  ├── preprocessing/ - scaper를 통해서 불러온 모델을 
  │       ├── to_csv.ipynb - scaper/output 폴더에 있는 json 파일을 하나의 csv로 만들어주는 ipynb파일 
  │       │ 
  │       ├── deprecated/ - R을 사용해서 전처리 할때 만든 20대 국회 전처리 모듈
  │              ├── preprocessing.R - scaper/output에 있는 json을 csv로 만들어주는 r파일 
  │              ├── to_onecsv.R - bill_result에 따라 나온 csv를 하나로 합쳐주고, 동명이인들을 확인하는 내용
  │ 
  ├── scraper/ - 참여연대 열려라 국회 사이트를 크롤링하는 scaper
          ├── searching_a_query.py - 크롤러를 작동시키는 실행파일
          ├── meta_scaper.ipynb - 현재 재임중인 국회의원들의 정보를 저장해주는 크롤러
          ├── usage.ipynb - 모듈을 test하는 ipynb
          │
          ├── output/ 크롤링된 결과물이 각 bill_result대로 들어가는 폴더
          │
          ├── Legisture_scraper/ 크롤링을 위해 만든 모듈이 저장되는 폴더
                          ├── parser.py
                          ├── scaper.py
                          ├── utils.py
  

