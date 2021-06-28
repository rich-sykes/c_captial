# py-order-book
Order book!

light weight order book module for aggregating equity positions.

Consumes thr following text streams

timestamp|order_id|action|ticker|side|price|size
str = "1568390201|abbb11|a|AAPL|B|209.00000|100"

timestamp - unix time
order_id - unqiue id
action - ('u', 'a' or 'c' - update, add or cancel)
ticker - equity id
side - ('b', 's' - buy or sell)
price
size - quantity 

