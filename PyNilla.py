from collections import deque
import itertools





try:
    izip_longest = itertools.izip_longest
except:
    izip_longest = itertools.zip_longest



def deint(value, base, alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    result = deque([])
    while value > 0:
        result.appendleft(value % base)
        value //= base
    if alphabet is None:
        return [digit for digit in result]
    elif not isinstance(alphabet, str):
        return [alphabet[digit] for digit in result]
    else:
        return "".join(alphabet[digit] for digit in result)
        
assert int(deint(314159, 16), 16) == 314159
    
    
def concat_ints(*values):
    if len(values) == 1:
        if isinstance(values[0], list):
            values = values[0]
        else:
            raise TypeError("can't expand the single arg.")
    result = 0
    for value in values:
        if value < 0:
            raise ValueError("negative value")
        result <<= value.bit_length()
        result += value
    return result
    
assert concat_ints(314, 159) == int(bin(314)[2:] + bin(159)[2:], 2)


def join(data, delimiter=""):
    return delimiter.join(str(item) for item in data)
    
assert "|".join(str(digit) for digit in [3,1,4,1,5,9]) == join([3,1,4,1,5,9], delimiter="|")

    
    
def _gen_lstrip(string, substring):
    stringItemGen = (item for item in string)
    memory = []
    for pair in izip_longest(stringItemGen, substring):
        memory.append(pair[0])
        if pair[1] is None:
            #successful match.
            del memory[:]
            break
        if pair[0] != pair[1]:
            break
    return itertools.chain()
    
    
def lstrip(string, substring):
    if hasattr(string, "__getitem__"):
        if string[:len(substring)] == substring:
            return string[len(substring):]
        return string
    else:
        if len(substring) == 0:
            return string
        return _gen_lstrip(string, substring)
            

assert lstrip("red=green", "red=") == "green"
        
        
        
        
def _gen_rstrip(string, substring):
    buffer = deque([None for i in range(len(substring))])
    cancellationProgress = 0
    for item in string:
        if item == substring[cancellationProgress]:
            cancellationProgress += 1
            if cancellationProgress == len(substring):
                return
        buffer.append(item)
        outputItem = buffer.popleft()
        if outputItem is not None:
            yield outputItem
        
        
def rstrip(string, substring):
    if hasattr(string, "__getitem__"):
        if string[-len(substring):] == substring:
            return string[:-len(substring)]
        return string
    else:
        if len(substring) == 0:
            return string
        return _gen_rstrip(string, substring)
            

assert rstrip("blue=yellow", "=yellow") == "blue"
        
        
        

def multi_replace(data, *args):
    if not isinstance(data, str):
        raise NotImplementedError("non str type")

    if len(args) == 1:
        pairGen = args[0]
    elif len(args) == 2:
        pairGen = zip(args[0], args[1])
    else:
      assert False

    for pair in pairGen:
        if isinstance(pair[0], str):
            data = data.replace(pair[0], pair[1])
        else:
            for strToReplace in pair[0]:
                data = data.replace(strToReplace, pair[1])
    return data

assert multi_replace("hello, world!", [("h","1"), ("e", "2"), ("l", "3")]) == "1233o, wor3d!"


def conditional_split(data_gen, activation_fun):
    exhaustionFlagHolder = [False]
    def genBetweenSplits():
        for item in data_gen:
            if activation_fun(item):
                return
            yield item
        exhaustionFlagHolder[0] = True
    while not exhaustionFlagHolder[0]:
        yield genBetweenSplits()
    return
    
    
def multi_split(data_gen, split_items):
    if len(split_items) > 3 and not isinstance(split_items, set):
        split_items = set(item for item in split_items)
    activationFun = (lambda testItem: testItem in split_items)
    return conditional_split(data_gen, activationFun)


"""
def _split_every_gen_only(data_gen, n, stop_flag):
    for i, item in enumerate(data_gen):
        yield item
        if i == n - 1:
            return
    stop_flag[0] = True


def split_every(data, n):
    dataGen = (item for item in data)
    stopFlag = [False]
    while True:
        yield _split_every_gen_only(dataGen, n, stopFlag)
        if stopFlag[0]:
            return
            
"""

def split_every(data, n):
    """
    thanks https://youtu.be/E_kZDvwofHY?t=1675
    """
    dataItemGen = (item for item in data)
    dataItemGenList = [dataItemGen for i in range(n)]
    return izip_longest(*dataItemGenList)
    


def gen_take_only(data, count):
    return itertools.islice(data,0,count,1)
    
def arr_take_only(data, count):
    return [item for item in gen_take_only(data, count)]
    
def arr_take_last(data, count):
    result = deque([])
    for item in data:
        result.append(item)
        while len(result) > count:
            result.popleft()
    return [item for item in deque]
    
def gen_rolling_window(data, n, include_start_partials=True, include_end_partials=True):
    currentWindow = deque([None for i in range(n)])
    
    if include_start_partials:
        yield [item for item in currentWindow]
        
    for i, item in enumerate(data):
        if item is None:
            raise ValueError("None encountered.")
        currentWindow.append(item)
        while len(currentWindow) > n:
            currentWindow.popleft()
        if include_start_partials or i + 1 >= n:
            yield [item for item in currentWindow]
        
    if include_end_partials:
        for i in range(n):
            currentWindow.popleft()
            currentWindow.append(None)
            assert len(currentWindow) == n
            yield [item for item in currentWindow]
        assert all(item is None for item in currentWindow)
    
    
    

def find_optimal(data, comparison_fun):
    optValueIndex, optValue = None, None
    for i, value in enumerate(data):
        if i == 0 or comparison_fun(value, optValue):
            optValueIndex, optValue = i, value
    return (optValueIndex, optValue)
    
"""
def find_optimals(data, comparison_fun):
    optEntries = []
    for i, value in enumerate(data):
        if i == 0 or comparison_fun(value, optEntries[0][1]):
            optEntries.append((i, value))
    return (optValueIndex, optValue)
"""
    
compare_less = lambda a, b: a < b
compare_greater = lambda a, b: a > b
    
    
def find_min(data):
    return find_optimal(data, compare_less)
    
    
def find_max(data):
    return find_optimal(data, compare_greater)
    
    
"""
todo:
  arbitrary base converter.

"""
    
