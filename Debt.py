import pyodbc

class TradeRecord:
    def __init__(self, source_currency, destination_currency, lots, price):
        self.source_currency = source_currency
        self.destination_currency = destination_currency
        self.lots = lots
        self.price = price


class TradeProcessor:
    LOT_SIZE = 100000.0

    def process_trades(self, stream):
        # --- Read lines from stream ---
        lines = [line.strip() for line in stream if line.strip()]

        trades = []
        line_count = 1

        for line in lines:
            fields = line.split(",")

            if len(fields) != 3:
                print(f"WARN: Line {line_count} malformed. Only {len(fields)} field(s) found.")
                line_count += 1
                continue

            if len(fields[0]) != 6:
                print(f"WARN: Trade currencies on line {line_count} malformed: '{fields[0]}'")
                line_count += 1
                continue

            try:
                trade_amount = int(fields[1])
            except ValueError:
                print(f"WARN: Trade amount on line {line_count} not a valid integer: '{fields[1]}'")
                line_count += 1
                continue

            try:
                trade_price = float(fields[2])
            except ValueError:
                print(f"WARN: Trade price on line {line_count} not a valid decimal: '{fields[2]}'")
                line_count += 1
                continue

            source_currency = fields[0][:3]
            destination_currency = fields[0][3:]

            trade = TradeRecord(
                source_currency,
                destination_currency,
                trade_amount / self.LOT_SIZE,
                trade_price
            )

            trades.append(trade)
            line_count += 1

        # --- Insert into database ---
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=TradeDatabase;"
            "Trusted_Connection=yes;"
        )

        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            try:
                for trade in trades:
                    cursor.execute(
                        "{CALL dbo.insert_trade (?, ?, ?, ?)}",
                        trade.source_currency,
                        trade.destination_currency,
                        trade.lots,
                        trade.price
                    )
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise

        print(f"INFO: {len(trades)} trades processed")
