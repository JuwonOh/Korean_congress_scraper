import argparse
import json
import os
import re
from Legisture_scraper import yield_law


def save(json_obj, directory):
    date = json_obj.get('date', '')
    title = json_obj.get('title', '')
    filepath = '{}/{}_{}.json'.format(directory,
                                      date, re.sub("[ \/:*?\<>|%]", "", title[:50]))
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(json_obj, fp, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str,
                        default='./output', help='Output directory')
    parser.add_argument('--sleep', type=float, default=.5,
                        help='Sleep time for each submission (post)')
    parser.add_argument('--max_page', type=int, default=100,
                        help='Number of scrapped articles page')
    parser.add_argument('--term_no', type=str,
                        default=21, help='Number of scrapped articles')
    parser.add_argument('--begin_date', type=str,
                        default='2020-06-05', help='Number of start documents')
    parser.add_argument('--end_date', type=str,
                        default='2022-07-18', help='Number of end documents')
    parser.add_argument('--bill_result', type=str,
                        default='철회', help='Number of scrapped articles')
    parser.add_argument('--verbose', dest='VERBOSE', action='store_true')

    args = parser.parse_args()
    directory = args.directory
    sleep = args.sleep
    term_no = args.term_no
    max_page = args.max_page
    begin_date = args.begin_date
    end_date = args.end_date
    bill_result = args.bill_result
    VERBOSE = args.VERBOSE

    # check output directory
    directory += '/%s' % bill_result
    if not os.path.exists(directory):
        os.makedirs(directory)

    n_exceptions = 0
    for article in yield_law(bill_result, max_page, end_date, begin_date, term_no):
        try:
            save(article, directory)
            print('scraped {}'.format(article.get('url'), ''))
        except Exception as e:
            n_exceptions += 1
            print(e)
            continue
        if n_exceptions > 0:
            print('Exist %d article exceptions' % n_exceptions)


if __name__ == '__main__':
    main()
