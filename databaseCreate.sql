--Creates a table that stores all user data
CREATE TABLE users (
	userID INT GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(50) UNIQUE NOT NULL,
	passwordhash BYTEA NOT NULL,
	cashBalance REAL NOT NULL,
	adminStatus BOOLEAN DEFAULT false,
	PRIMARY KEY(userID)
);

---Creates a table that stores all stock data
CREATE TABLE stocks (
	stockTicker VARCHAR(10) NOT NULL UNIQUE,
	regionname VARCHAR(50) NOT NULL,
	stockPrice REAL NOT NULL,
	stockVolume INT NOT NULL,
	stockMarketCap REAL NOT NULL
);

---Creates a table that stores all data relating to user stock holdings
CREATE TABLE stockHoldings(
	stockTicker VARCHAR(10) NOT NULL UNIQUE,
	stockholder INT NOT NULL,
	volumeOwned INT NOT NULL,
	purchasePrice REAL NOT NULL,
	totalValue REAL NOT NULL,
	PRIMARY KEY (stockTicker, stockHolder),
	CONSTRAINT fk_stockHolder
		FOREIGN KEY (stockholder)
			REFERENCES users(userID)
);

---Creates a table that stores all currently open trades in the queue
CREATE TABLE openTrades (
	tradeID INT GENERATED ALWAYS AS IDENTITY,
	userID INT NOT NULL,
	tradeType VARCHAR(8) NOT NULL,
	ticker VARCHAR(10) NOT NULL,
	quantStock INT NOT NULL,
	stockRemaining INT NOT NULL,
	stockPrice INT NOT NULL,
	totalTradeValue INT NOT NULL,
	tradeOpened TIMESTAMP,
	PRIMARY KEY (tradeID),
	CONSTRAINT fk_userID
		FOREIGN KEY (userID)
			REFERENCES users(userID),
	CONSTRAINT fk_stockTicker
		FOREIGN KEY (ticker)
			REFERENCES stocks(stockTicker)
);

---Creates a table that stores all the stored trades
CREATE TABLE closedTrades (
	tradeID INT GENERATED ALWAYS AS IDENTITY,
	userID INT NOT NULL,
	ticker VARCHAR(10) NOT NULL,
	tradeType VARCHAR(8) NOT NULL,
	quantStock INT NOT NULL,
	stockPrice INT NOT NULL,
	tradeClosed TIMESTAMP,
	PRIMARY KEY (tradeID),
	CONSTRAINT fk_userID
		FOREIGN KEY (userID)
			REFERENCES users(userID)
);

CREATE TABLE apiKeys (
	accID INT NOT NULL,
	apikey VARCHAR(40) NOT NULL,
	revoked BOOLEAN DEFAULT false,
	PRIMARY KEY (apiKey),
	CONSTRAINT fk_stockHolder
		FOREIGN KEY (stockholder)
			REFERENCES users(userID)
)
