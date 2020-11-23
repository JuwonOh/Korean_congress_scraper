# Korean_congress_scraper

20대 국회의원들의 개인 표결 기록을 수집하기 위한 크롤러입니다. 의원 개인의 인적정보와 소속정당과 법안 표결, 표결 내용를 수집합니다.

## Guide

### Data source

korean_congress_scraper는 세가지 사이트에서 데이터를 수집합니다. 
의원 개인의 인적정보에 대한 데이터를 공공데이터 포털의 의원정보 api(https://www.data.go.kr/dataset/15012647/openapi.do)에서 제공하는 자료를 사용합니다.
의회에서 이뤄지는 법안에 대한 표결 정보는 2가지 사이트에서 수집합니다. 
먼저 참여연대 열려라 국회(http://watch.peoplepower21.org/index.php)에서 제공하는 법안 정보를 수집합니다.
하지만 열려라 국회는 동명이인을 구별하지 않기때문에, 보조적으로 국회 의안정보 시스템(http://likms.assembly.go.kr/bill/main.do)를 사용해서, 이름이 동일한 의원들의 표결기록을 수집했습니다.

### Usage guide

scraper의 searching_a_query.py를 통해 참여연대 열려라 국회에서 제공하는 의원의 표결자료를 수집할 수 있습니다. 
searching_a_query.py에서 지정 할 수 있는 조건은 4가지입니다. 
bill_result는 법안의 결과를 기준으로 표결결과를 수집합니다. "부결", "원안가결", "수정가결"이 가능합니다. 
max_page는 수집할 법안의 수를 지정할 수 있습니다. 
begin_date에는 원하는 기간의 첫날을, end_date에는 원하는 기간의 마지막 날을 적으면 됩니다.
예를 들어 searching_a_query.py --bill_result "원안가결" --max_page "10" --begin_date "2017-01-01" -- end_date "2018-01-01"을 지정하면, 2017년 1월 1일부터 2018년 1월 1일까지 원안가결된 법안이 10000개의 표결기록을 수집합니다.

의안정보 시스템의 크롤링은 의원 개인의 표결 기록에 대한 html파일이 필요합니다. 이는 차후에 보완될 것입니다.

### Property

이 크롤러는 브리티쉬 컬럼비아 대학교 정치학과 Gyung-Ho Jeong 교수님과의 작업을 기초로 한 것입니다.

