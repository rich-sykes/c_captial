import pandas as pd
import re

class OrderBook:

    def __init__(self):
        self.name = "order book"
        self.order_book = self.init_order_book()

    # initalise new order book
    def init_order_book(self):

        param = ['timestamp', 'order_id', 'action', 'ticker', 'side', 'price', 'size']
        new_order_book = pd.DataFrame(columns=param)
        new_order_book = new_order_book.set_index('order_id')

        return new_order_book

    # read data stream
    def read_ds(self, msg_str):

        """
        Convert data stream into list.
        - Returns an empty list in event of failure.
        :param msg_str:
        :return:
        """

        try:
            msg_list = msg_str.split('|')
        except Exception as e:
            msg_list = list()

        return msg_list

    # validate message [a,u,c,e]
    def validate_ds(self, msg_list):

        """
        Convert list into dict of message components.
        - if there is an error in the consumption, action is returned as "e".
        :param msg_list:
        :return:
        """

        # pre allocate "message" dict
        message = dict()

        # all message must be at least 3 parameters long (timestamp, order id, action).
        if len(msg_list) >= 3:

            # cancel - timestamp, order id, action
            if len(msg_list) == 3:
                # 'timestamp'
                message['timestamp'] = int(msg_list[0])
                # 'order_id'
                message['order_id'] = str(msg_list[1])
                # 'action'
                if msg_list[2] in ['c']:
                    message['action'] = str(msg_list[2])
                else:
                    message['action'] = 'e'

                return message

            # update - timestamp, order id, action and size
            if len(msg_list) == 4:
                # 'timestamp'
                message['timestamp'] = int(msg_list[0])
                # 'order_id'
                message['order_id'] = str(msg_list[1])
                # 'action'
                if msg_list[2] in ['u', 'c']:
                    message['action'] = str(msg_list[2])
                else:
                    message['action'] = 'e'
                # 'size'
                message['size'] = int(msg_list[3])
                return message

            # add - timestamp, order id, action, ticker, side, price and size
            elif len(msg_list) == 7:
                # 'timestamp'
                message['timestamp'] = int(msg_list[0])
                # 'order_id'
                message['order_id'] = str(msg_list[1])
                # 'action' - must be add, update or cancel
                if msg_list[2] in ['a', 'u', 'c']:
                    message['action'] = str(msg_list[2])
                else:
                    message['action'] = 'e'
                # 'ticker'
                message['ticker'] = str(msg_list[3])
                # 'side'
                if msg_list[4] in ['B', 'S']:
                    message['side'] = str(msg_list[4])
                else:
                    message['action'] = 'e'
                    return message
                # 'price'
                message['price'] = float(msg_list[5])
                # 'size'
                message['size'] = int(msg_list[6])
                return message

        # error fall back
        else:
            message['action'] = 'e'
            return message

    # add_order
    def add_order(self, message):
        # print("add order")
        order = pd.Series(message, name=message['order_id'])
        order_book = self.order_book.append(order[['timestamp', 'action', 'ticker', 'side', 'price', 'size']])

        # sort order book
        order_book.sort_values(['ticker', 'side', 'price', 'timestamp'], inplace=True)

        return order_book

    # update_order
    def update_order(self, message):
        # print("update order")
        # dict to series
        order = pd.DataFrame(message, index=[1]).set_index('order_id')
        order_book = self.order_book
        order_book.update(order)

        # sort order book
        order_book.sort_values(['ticker', 'side', 'price', 'timestamp'], inplace=True)

        return order_book

    # cancel_order
    def cancel_order(self, message):
        # print("cancel order")
        order_book = self.order_book
        order_book.drop(message['order_id'], inplace=True)

        # sort order book
        order_book.sort_values(['ticker', 'side', 'price', 'timestamp'], inplace=True)

        return order_book

    # action request
    def post_order(self, msg_str):

        # read string to list
        msg_list = self.read_ds(msg_str)

        # create message structure
        message = self.validate_ds(msg_list)

        if message['action'] == 'e':
            # error
            return -1
        elif message['action'] == 'a':
            # add order
            self.order_book = self.add_order(message=message)
        elif message['action'] == 'u':
            # update order
            self.order_book = self.update_order(message=message)
        elif message['action'] == 'c':
            # cancel order
            self.order_book = self.cancel_order(message=message)
        else:
            # report error
            return -1

        return 0

    # get best price
    def get_best_price(self, ticker):

        result = dict()
        simple_orderbook = self.order_book[['ticker', 'side', 'price']].sort_values(['price', 'ticker', 'side'])


        if simple_orderbook['ticker'].str.contains(ticker).any():

            try:
                result['bid'] = simple_orderbook[
                    (simple_orderbook['ticker'] == ticker) & (simple_orderbook['side'] == 'B')]['price'].max()
            except Exception as e:
                result['bid'] = 0

            try:
                result['ask'] = simple_orderbook[
                    (simple_orderbook['ticker'] == ticker) & (simple_orderbook['side'] == 'S')]['price'].min()
            except Exception as e:
                result['ask'] = 0

        else:
            result['bid'] = 0
            result['ask'] = 0


        return result


def processOrder(orderbook, order):

    """
    This function add / update or cancel an order in the order book
    * orderBook is a data structure maintaining the orders (choose / implement it as you wish)
    * order is an order in the pipe delimited string format shown above

    :param orderbook: orderbook object
    :param order: data stream str
    :return: nothing
    """
    try:
        result = orderbook.post_order(order)

    except Exception as e:
        # print(str(e))
        result = -1
        return result

def getBestBidAndAsk(orderbook, ticker):

    """
    This function gets the best bid and ask for the specified ticker
    - If no ticket is present, return 0 for both bid and ask.
    :param orderbook:
    :param ticker:
    :return:
    """

    return orderbook.get_best_price(ticker=ticker)










