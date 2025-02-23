import time, os

# Decoration
def timeit(func):
    '''
    Decoration function to count time consuming.
    '''
    def wrap(*args, **kwargs):
        t_0 = time.time()
        result = func(*args, **kwargs)
        print_cust("Computation Time Info:\tThe '{}' Function takes {:<5.2f}s.".format(func.__name__, time.time()-t_0), 'yellow')
        return result
    return wrap

#printSeries
def print_cust(info, color:str='black', end='\n'):
    if isinstance(info, str):
        head = info[:7].lower()
        if head == 'success':
            color = 'green'
        elif head == 'warning':
            color = 'red'
    end_t = '\033[0m'
    colors = {'green':'\033[32m', 'black':'\033[30m', 'red':'\033[31m', 'yellow':'\033[33m', \
              'blue': '\033[34m', 'white':'\033[37m'}
    try:
        assert color in colors.keys()
    except:
        print(f"{colors['red']}Warning: {color} is not in the list, use blue as default.{end_t}", end=end)
    print(f"{colors[color]}{info}{end_t}", end=end)


# directorySeries
def makedirs(path:os.PathLike, rewrite=False, show=True):
    if os.path.exists(path):
        if not rewrite:
            raise FileExistsError(f"The directory {path} is already existed, continue will be replaced. \
                                  Pls check it out.")
    try:
        os.mkdir(path)
    except:
        print_cust(f"Warning: The root directory is not existed yet, has already create those directories.")
        os.makedirs(path)

    print_cust(f"Successfully increased the directory: {os.path.abspath(path)}", 'green')


# timeSeries
def getLocalTime(timeFormat=False, show=False):
    timestamp = time.time()
    if timeFormat:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    else:
        current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime(timestamp))
    if show:
        print(current_time)
    return current_time