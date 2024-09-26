# -*- coding: utf-8 -*-
#
#   Dynamic Betting Strategy: Adjusts bet amount dynamically based on external factors.
#
from typing import Union, List, Dict, Tuple, Any

REQUIRED_FIELDS = ("confidence", "bet_amount_per_threshold", "market_trend", "last_bet_outcome")


def check_missing_fields(kwargs: Dict[str, Any]) -> List[str]:
    """Check for missing fields and return them, if any."""
    missing = []
    for field in REQUIRED_FIELDS:
        if kwargs.get(field, None) is None:
            missing.append(field)
    return missing


def remove_irrelevant_fields(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Remove the irrelevant fields from the given kwargs."""
    return {key: value for key, value in kwargs.items() if key in REQUIRED_FIELDS}


def dynamic_bet_amount(
    confidence: float,
    bet_amount_per_threshold: Dict[str, int],
    market_trend: float,
    last_bet_outcome: str
) -> Dict[str, Union[int, Tuple[str]]]:
    """Adjust the bet amount based on confidence and external factors."""
    
    threshold = str(round(confidence, 1))
    base_bet_amount = bet_amount_per_threshold.get(threshold, None)

    if base_bet_amount is None:
        return {
            "error": (
                f"No amount was found in {bet_amount_per_threshold=} for {confidence=}.",
            )
        }

    # Adjust based on market trend (example: increase bet if market trend is positive)
    adjusted_bet_amount = base_bet_amount * (1 + market_trend)

    # Increase bet if the last bet was a loss
    if last_bet_outcome == "loss":
        adjusted_bet_amount *= 1.5  # Increase by 50% if last bet was a loss

    return {"bet_amount": int(adjusted_bet_amount)}


def run(*_args, **kwargs) -> Dict[str, Union[int, Tuple[str]]]:
    """Run the strategy."""
    missing = check_missing_fields(kwargs)
    if len(missing) > 0:
        return {"error": (f"Required kwargs {missing} were not provided.",)}

    kwargs = remove_irrelevant_fields(kwargs)
    return dynamic_bet_amount(**kwargs)
