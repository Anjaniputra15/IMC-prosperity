from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict, Any
import string
import math
import json

class Trader:
    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        result = {}
        conversions = 0
        trader_data = ""

        if state.traderData:
            try:
                past_state = json.loads(state.traderData)
            except json.JSONDecodeError:
                past_state = {}
        else:
            past_state = {}

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: list[Order] = []

            result[product] = orders

        trader_data = json.dumps(past_state)

        return result, conversions, trader_data



def main():
    pass


if __name__ == "__main__":
    main()
