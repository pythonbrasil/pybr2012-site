#!/usr/bin/env python
# coding: utf-8

import csv
import datetime

import requests
import xmltodict


class PagSeguro(object):
    URL_TRANSACTIONS = 'https://ws.pagseguro.uol.com.br/v2/transactions'
    URL_TRANSACTION_DETAIL = \
            'https://ws.pagseguro.uol.com.br/v2/transactions/{}'

    def __init__(self, email, token):
        self.__parameters = {'email': email, 'token': token}

    def get_transactions(self, initial_date, final_date):
        '''Get all transactions in the interval

        If more than one page is needed, it automatically gets ALL the pages.
        `initial_date` and `final_date` should be in format
        `YYYY-MM-DDTHH:MM:SS`.
        PagSeguro's API documentation says it must be `YYYY-MM-DDTHH:MM:SS.sz`,
        where 's' is microseconds and 'z' is timezone, but it is not needed and
        it fails in some cases!
        '''
        page = 1
        max_results = 100
        finished = False
        parameters = {'initialDate': initial_date, 'finalDate': final_date,
                      'maxPageResults': max_results}
        parameters.update(self.__parameters)
        transactions = []
        while not finished:
            parameters['page'] = page
            response = requests.get(self.URL_TRANSACTIONS, params=parameters)
            data = xmltodict.parse(response.text.encode('iso-8859-1'))
            result = data['transactionSearchResult']
            if int(result['resultsInThisPage']) > 0:
                new_transactions = result['transactions']['transaction']
                if type(new_transactions) is not list: # only one returned
                    new_transactions = [new_transactions]
                transactions.extend(new_transactions)
            total_pages = int(result['totalPages'])
            if page < total_pages:
                page += 1
            elif page == total_pages:
                finished = True
        return transactions

    def get_transaction(self, transaction_id):
        '''Given a transaction id, get its information'''
        url = self.URL_TRANSACTION_DETAIL.format(transaction_id)
        response = requests.get(url, params=self.__parameters)
        print response.status_code, response.text
        return xmltodict.parse(response.text.encode('iso-8859-1'))['transaction']

if __name__ == '__main__':
    email = "" #TODO: put your PagSeguro email
    token = "" #TODO: put your PagSeguro token here
    ps = PagSeguro(email, token)

    def get_all_transactions():
        '''Get past transactions and save it to a CSV file

        PagSeguro only allow us to get 6-months-old transactions.
        '''

        # Get all desired transactions
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        dates = ['2012-06-01', '2012-07-01', '2012-08-01', '2012-09-01',
                 '2012-10-01', '2012-11-01', now]
        pairs = zip(dates, dates[1:]) # put in (start, end) form
        whole_transactions = []
        for start, end in pairs:
            start += 'T00:00:00-02:00'
            end += 'T00:00:00-02:00'
            print start, end,
            transactions = ps.get_transactions(start, end)
            print len(transactions)
            whole_transactions.extend(transactions)

        # Now save it!
        my_csv_fp = open('transactions.csv', 'w')
        my_csv = csv.writer(my_csv_fp)
        keys = ['code', 'status', 'paymentMethod', 'grossAmount', 'feeAmount',
                'netAmount', 'lastEventDate', 'reference']
        for transaction in whole_transactions:
            transaction['paymentMethod'] = transaction['paymentMethod']['type']
            row = []
            for key in keys:
                try: # some rows just don't have 'reference' :-/
                    value = transaction[key].encode('utf-8')
                except KeyError:
                    value = ''
                row.append(value)
            my_csv.writerow(row)
        my_csv_fp.close()
