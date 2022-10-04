import logging
from collections import OrderedDict

# bioinfobot imports
from bioinfobot.utils.paths import TweetAnalysisPaths


# starting logger
ta_paths = TweetAnalysisPaths()
logging.basicConfig(
    filename=ta_paths.analysis_log,
    level=logging.DEBUG,
    filemode="a",
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


def flatten_list(nd_list):
    """flattens N-d list into 1D list

    Parameters
    ----------
    nd_list : list
        List containing nested lists

    Returns
    -------
    list
        1D list of elements

    Raise
    -----
    TypeError
        Raised if the input parameter is not a list
    """
    if not isinstance(nd_list, list):
        func_name = flatten_list.__name__
        logging.error(f"Invalid data type capture in {func_name}")
        raise TypeError("nd_list must be a list")

    flat_list = []
    for elm in nd_list:
        if isinstance(elm, list):
            flattenlist = flatten_list(elm)
            flat_list += flattenlist
        else:
            flat_list.append(elm)

    return flat_list


def dict_value_sort_return_top(frequency_dict, maxreturn):
    """Sort the dictionary according to values and return a list of top n elements"""
    dictionary_sorted = OrderedDict(
        sorted(frequency_dict.items(), key=lambda t: t[1], reverse=True)
    )
    # Store top values in an array
    # Change maxCount value to extract top n elements
    count = 0
    top_elements = []
    for k, v in dictionary_sorted.items():
        # Key and value pairs are stored in the form of a tuple in the topWords array
        # Another dictionary is not created here in order to preserve the sorted order
        top_elements.append((k, v))
        count += 1
        if count >= maxreturn:
            break
    return top_elements
