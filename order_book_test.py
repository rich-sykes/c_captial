import unittest

from main import OrderBook
from main import processOrder, getBestBidAndAsk


class TestMethods(unittest.TestCase):

    def test_order_book(self):
        
        # create an order book
        orderbook = OrderBook()

        self.assertEqual(orderbook.name, 'order book')

    def test_stream_1(self):
        
        # create an order book
        orderbook = OrderBook()

        # steam 1
        processOrder(orderbook, "1568390201|abbb11|a|AAPL|B|209.00000|100")
        processOrder(orderbook, "1568390244|abbb11|u|101")
        processOrder(orderbook, "1568390245|abbb11|c")

        self.assertEqual(orderbook.name, 'order book')

    def test_stream_2(self):
        
        # create an order book
        orderbook = OrderBook()

        # steam 2
        processOrder(orderbook, "1568390201|abbb11|a|AAPL|B|209.00000|100")
        processOrder(orderbook, "1568390202|abbb12|a|AAPL|S|210.00000|10")
        processOrder(orderbook, "1568390204|abbb11|u|10")
        processOrder(orderbook, "1568390203|abbb12|u|101")
        processOrder(orderbook, "1568390245|abbb11|c")

        self.assertEqual(orderbook.name, 'order book')

    def test_bad_string(self):
        
        # create an order book
        orderbook = OrderBook()

        # steam 2
        processOrder(orderbook, "1568390201|abbb11|a|AAPL|B|209.00000|100")
        processOrder(orderbook, "1568390202|abbb12|a|AAPL|S|210.00000|10")
        processOrder(orderbook, "1568390204|abbb11|u|10")
        processOrder(orderbook, "1568390203|abbb12|u|101")
        processOrder(orderbook, "1568390245|abbb11|c")

        # testing - incorrect string
        processOrder(orderbook, "1568390201|abbb11|f|AAPL|B|209.00000|100")

        self.assertEqual(len(orderbook.order_book), 1)

    def test_multi_ticker(self):
        
        # create an order book
        orderbook = OrderBook()

        # testing multiple tickers
        
        # - add buys
        processOrder(orderbook, "1568390201|abbb13|a|AAPL|B|297.43|33")
        processOrder(orderbook, "1568390202|abbb14|a|MSFT|B|158.62|62")
        processOrder(orderbook, "1568390204|abbb15|a|AMZN|B|1874.9|5")
        processOrder(orderbook, "1568390205|abbb16|a|FB|B|208.67|48")
        processOrder(orderbook, "1568390206|abbb17|a|MSFT|B|160.62|3")
        processOrder(orderbook, "1568390207|abbb18|a|FB|B|210|5")

        # - add sells
        processOrder(orderbook, "1568390208|abbb19|a|AAPL|S|310.43|100")
        processOrder(orderbook, "1568390209|abbb20|a|MSFT|S|190|6")
        processOrder(orderbook, "1568390210|abbb21|a|AMZN|S|2000|200")
        processOrder(orderbook, "1568390211|abbb22|a|FB|S|220|5")
        processOrder(orderbook, "1568390212|abbb23|a|FB|S|230|5")

        # - cancel a mistaken order
        processOrder(orderbook, "1568390213|abbb23|c")

        # - update
        processOrder(orderbook, "1568390214|abbb14|u|67")
        processOrder(orderbook, "1568390215|abbb17|u|10")
        processOrder(orderbook, "1568390216|abbb19|u|195")
        processOrder(orderbook, "1568390217|abbb21|u|205")

        # - add sells
        processOrder(orderbook, "1568390218|abbb24|a|FB|S|223.76|5")
        processOrder(orderbook, "1568390219|abbb25|a|FB|S|240|500")
        processOrder(orderbook, "1568390220|abbb13|a|AAPL|B|280.34|13")

        self.assertEqual(len(orderbook.order_book), 13)

    def test_get_prices(self):
        
        # create an order book
        orderbook = OrderBook()

        # testing multiple tickers
        
        # - add buys
        processOrder(orderbook, "1568390201|abbb13|a|AAPL|B|297.43|33")
        processOrder(orderbook, "1568390202|abbb14|a|MSFT|B|158.62|62")
        processOrder(orderbook, "1568390204|abbb15|a|AMZN|B|1874.9|5")
        processOrder(orderbook, "1568390205|abbb16|a|FB|B|208.67|48")
        processOrder(orderbook, "1568390206|abbb17|a|MSFT|B|160.62|3")
        processOrder(orderbook, "1568390207|abbb18|a|FB|B|210|5")

        # - add sells
        processOrder(orderbook, "1568390208|abbb19|a|AAPL|S|310.43|100")
        processOrder(orderbook, "1568390209|abbb20|a|MSFT|S|190|6")
        processOrder(orderbook, "1568390210|abbb21|a|AMZN|S|2000|200")
        processOrder(orderbook, "1568390211|abbb22|a|FB|S|220|5")
        processOrder(orderbook, "1568390212|abbb23|a|FB|S|230|5")

        # - cancel a mistaken order
        processOrder(orderbook, "1568390213|abbb23|c")

        # - update
        processOrder(orderbook, "1568390214|abbb14|u|67")
        processOrder(orderbook, "1568390215|abbb17|u|10")
        processOrder(orderbook, "1568390216|abbb19|u|195")
        processOrder(orderbook, "1568390217|abbb21|u|205")

        # - add sells
        processOrder(orderbook, "1568390218|abbb24|a|FB|S|223.76|5")
        processOrder(orderbook, "1568390219|abbb25|a|FB|S|240|500")
        processOrder(orderbook, "1568390220|abbb13|a|AAPL|B|280.34|13")


        # - get prices
        getBestBidAndAsk(orderbook, 'AAPL')
        getBestBidAndAsk(orderbook, 'AMZN')
        getBestBidAndAsk(orderbook, 'FB')
        getBestBidAndAsk(orderbook, 'MSFT')

        # - get prices for ticker
        result = getBestBidAndAsk(orderbook, 'FB')

        self.assertEqual(result['bid'], 210)

    def test_get_prices_missing_ticker(self):
        
        # create an order book
        orderbook = OrderBook()

        # testing multiple tickers
        
        # - add buys
        processOrder(orderbook, "1568390201|abbb13|a|AAPL|B|297.43|33")
        processOrder(orderbook, "1568390202|abbb14|a|MSFT|B|158.62|62")
        processOrder(orderbook, "1568390204|abbb15|a|AMZN|B|1874.9|5")
        processOrder(orderbook, "1568390205|abbb16|a|FB|B|208.67|48")
        processOrder(orderbook, "1568390206|abbb17|a|MSFT|B|160.62|3")
        processOrder(orderbook, "1568390207|abbb18|a|FB|B|210|5")

        # - add sells
        processOrder(orderbook, "1568390208|abbb19|a|AAPL|S|310.43|100")
        processOrder(orderbook, "1568390209|abbb20|a|MSFT|S|190|6")
        processOrder(orderbook, "1568390210|abbb21|a|AMZN|S|2000|200")
        processOrder(orderbook, "1568390211|abbb22|a|FB|S|220|5")
        processOrder(orderbook, "1568390212|abbb23|a|FB|S|230|5")

        # - cancel a mistaken order
        processOrder(orderbook, "1568390213|abbb23|c")

        # - update
        processOrder(orderbook, "1568390214|abbb14|u|67")
        processOrder(orderbook, "1568390215|abbb17|u|10")
        processOrder(orderbook, "1568390216|abbb19|u|195")
        processOrder(orderbook, "1568390217|abbb21|u|205")

        # - add sells
        processOrder(orderbook, "1568390218|abbb24|a|FB|S|223.76|5")
        processOrder(orderbook, "1568390219|abbb25|a|FB|S|240|500")
        processOrder(orderbook, "1568390220|abbb13|a|AAPL|B|280.34|13")

        # - get prices for missing ticker
        result = getBestBidAndAsk(orderbook, 'ENE')


        self.assertEqual(result['bid'], 0)


if __name__ == '__main__':
    unittest.main()

# eof
