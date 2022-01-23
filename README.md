# The Alicolliar Technicolour Wonderland Stock Exchange
### A new, innovative, not-total-shite stock exchange for DemocracyCraft
[![Build Status](https://app.travis-ci.com/Alicolliar/MCInvest-privy.svg?token=X8u6HjgJuEdtxH7zArUD&branch=production)](https://app.travis-ci.com/Alicolliar/MCInvest-privy)

## Reason for.... existence
There are 3 reasons this exists:
- Spite
- I wanted to build it, because I don't go outside and these things interest me.
- I realised I could use it to fulfil a uni project

## What makes this... interesting
There are things that make this interesting to different people, for DemocracyCraft it's probably:
- The near full automation
- The fact there is now competition (ooh) to those scum at Onyx

Things that make this interesting to me:
- The trade matching system (further explained below)
- The fact I can get free marks on my uni project, yay

## The aforementioned Trade Matching system, explained
#### What most exchanges do
The majority of virtual exchanges simply trade into "a void", known handwaved away as "the exchange". For example, you have stock ABC, to buy stock ABC you submit a buy order, the order is then immediately fulfilled from *the void*, and then all is thusly well.
#### A misrepresentation of IRL exchanges
Of course, this isn't how a real market works, in an IRL market you wait for someone to fill the opposite end of your trade (i.e. for every buy there is a sell, and for every sell, a buy), but virtual markets generally don't have a large enough volume of trades to simulate this.
#### How my, non-patent, Trade Matching System works
The lifecycle of a standard buy trade in this exchange is thus (the trade is for 100 stock of ABC company at £100):
- The user submits the trade, which goes into the "Open Trade" queue
- If someone else submits an "opposing" trade (let's say a trade to sell 20 ABC at £105) at +-10% of the same price, then that order is filled with that trade, if the order would fill more than 1 trade, then it does that, keeping going until the opposing trade has run out of stock to trade.

## Notes on customisability
While, yes, this is being specifically designed to work with DemocracyCraft, the manner in which the cash system has been designed (i.e. DC won't give me an API for economy) means that, technically, you can adjust the cashTransaction function and include any ol' thing in the deposit/withdrawal functions, thus with a little programming magic you too can make it work with your working API, you lucky git, you.

## To-do List
This is a MoSCoW style to-do list, which lets me tick things off and 'at.
### Must do
(Things what have to be done)
- [x] - Fully functioning trade execution page, backend and TradeMatching at 10% spread
- [x] - Login/Signup Pages, with all the functionality
- [x] - Super-User Administration Page
- [x] - Portfolio View Page
- [x] - A price logging function/module, possibly run on a cron job on the App Engine instance itself - I'll find a way to run logTimes.py every hour
- [x] - A base stock view page, with downloads for past prices
- [x] - The backend for all internal, and internal-external cash transactions
- [x] - A pretty web design, with nice templates and pages

### Should Have
(Immediate Stretch Goals)
- [x] - An “enhanced” stock view page, with graphs, statistics points and possibly others.
- [ ] - List the total value of the market quickly
- [x] - List the top 10 largest value open trades on the homepage - (Technically completed, as all open trades are displayed)
- [ ] - List the 5 most recently closed trades on the homepage
- [ ] - Expansion of the accounts system, to allow specific accounts for regulators and institutional investors
- [x] - A way for regulators to access CSVes of trades and cash transacts - (Technical completion again, as admins can download)

### Could have
(Slightly further stretch goals)
- [ ] - Expansion of the admin pages, to allow for more specific administrators with limited powers (namely "investor liaison", "institutional liaison", "company liaison", "regulator liaison")
- [ ] - An API for traders to access prices and other data about stocks, but *VERY MUCH NOT* submit trades

### Would have
(Not even stretch goals at this point)
- [ ] - A complete database connection refactor to use a NoSQL database that’s significantly faster
- [ ] - Rate-limited API expansion for institutional investors that allows them to submit trades
- [ ] - A lower rate-limited, (virtually) paid-for API that allows institutions to submit faster trades for Higher Frequency Trading
- [ ] - An almost separate-but-the-same market for trading futures, thus providing significantly higher leveraged trades to users. This can also introduce a commodities trading market, which opens up the market to those wiling to invest more and more. (I am moderately aware that, at this point, the numbers have crossed "make believe" into "pure randomness", but that's interesting).


## Notes
Any commit from 28e39ec98b906410d2a4734c21b25ae5653f1e86 is part of my uni project thing, so umm yeah
