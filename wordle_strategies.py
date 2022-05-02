from presorted_list_word_scorer import PresortedListWordScorer
import wordle_dict as wd
from word_frequency_strategy import WordFrequencyStrategy
from wordle_strategy import WordleStrategy
from positional_frequency_scorer import PositionalFrequencyWordScorer
import log_config  # import does logging config


def build_default_strategy() -> WordleStrategy:
    # These settings were experimentally determined to be the best chance of success, and lowest average number of guesses
    settings = {"max_guesses": 1, "first_word": "cares"}
    return build_strategy_from_name("CombinedWordScore", settings)


def build_strategy_from_name(strat_name: str, exploration_settings: map = None):
    if strat_name == "CombinedWordScore":
        return combined_word_score_strategy(exploration_settings)
    elif strat_name == "LetterFrequencyList":
        return letter_frequency_list_strategy(exploration_settings)
    elif strat_name == "LetterFrequency":
        return WordleStrategy(lambda: PositionalFrequencyWordScorer(
            wd.load_dictionary()), exploration_settings)
    elif strat_name == "WordFrequency":
        return WordFrequencyStrategy()
    else:
        raise ValueError(f"Unknown strategy: {strat_name}")


def combined_word_score_strategy(exploration_settings: map = None) -> WordleStrategy:
    words = wd.load_combined_word_score_dictionary()
    return WordleStrategy(lambda: PresortedListWordScorer(
        wd.load_combined_word_score_dictionary()), exploration_settings)


def letter_frequency_list_strategy(exploration_settings: map = None) -> WordleStrategy:
    return WordleStrategy(lambda: PresortedListWordScorer(
        wd.load_position_frequency_dictionary()), exploration_settings)
