# coding: utf-8
import datetime

import requests
import xmltodict

from django.conf import settings

from pythonbrasil8.subscription import models


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
                if type(new_transactions) is not list:  # only one returned
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
    email = settings.PAGSEGURO["email"]
    token = settings.PAGSEGURO["token"]
    ps = PagSeguro(email, token)

    def get_all_transactions():
        '''Get past transactions and save it to a CSV file

        PagSeguro only allow us to get 6-months-old transactions.
        '''

        # Get all desired transactions
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        start = yesterday.strftime('%Y-%m-%dT%H:%M:%S-02:00')
        end = now.strftime('%Y-%m-%dT%H:%M:%S-02:00')
        whole_transactions = ps.get_transactions(start, end)

        paid = [t for t in whole_transactions
                if 'reference' in t
                and t['status'] in ('3', '4')
                and t['grossAmount'] in ('150.00', '250.00', '350.00')]
        for transaction in paid:
            subscription_id = transaction['reference']
            transactions = models.Transaction.objects.select_related('subscription').filter(
                subscription_id=subscription_id,
                price=float(transaction['grossAmount']),
            )
            update = None
            for transaction in transactions:
                if transaction.status == 'pending':
                    update = transaction
                elif transaction.status == 'done':
                    update = None
                    break
            if update:
                update.status = 'done'
                update.save()
                update.subscription.status = 'confirmed'
                update.subscription.save()
    get_all_transactions()
