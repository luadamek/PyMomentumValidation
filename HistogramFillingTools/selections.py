

def range_selection_function(event, variable, range_low, range_hi):
    return (event[variable] < range_hi) & (range_low < event[variable])
