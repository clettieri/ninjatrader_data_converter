# ninjatrader_data_converter
Converts Spryware tick data for use in NinjaTrader

This makes several assumptions about the data format you have and the data format you would like.

Assuming you have a CSV of tick data for stocks with columns of ["Date", "Time", "Symbol", "TransType", "ItemType", 
"Condition", "Scale", "Sequence", "Exchange", "Price", "Size"].

Will convert to a CSV of tick data with columns of yyyyMMdd HHmmss;price;volume, for use in NinjaTrader8.

Uses pandas to parse and alter data.
