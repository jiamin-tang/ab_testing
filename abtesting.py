from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import chi2

from abtesting_test import *

# You can comment out these lines! They are just here to help follow along to the tutorial.
# print(t_dist.cdf(-2, 20)) # should print .02963
# print(t_dist.cdf(2, 20)) # positive t-score (bad), should print .97036 (= 1 - .2963)

# print(chi2.cdf(23.6, 12)) # prints 0.976
# print(1 - chi2.cdf(23.6, 12)) # prints 1 - 0.976 = 0.023 (yay!)

# TODO: Fill in the following functions! Be sure to delete "pass" when you want to use/run a function!
# NOTE: You should not be using any outside libraries or functions other than the simple operators (+, **, etc)
# and the specifically mentioned functions (i.e. round, cdf functions...)

def slice_2D(list_2D, start_row, end_row, start_col, end_col):
    '''
    Splices a the 2D list via start_row:end_row and start_col:end_col
    :param list: list of list of numbers
    :param nums: start_row, end_row, start_col, end_col
    :return: the spliced 2D list (ending indices are exclsive)
    '''
    to_append = []
    for l in range(start_row, end_row):
        to_append.append(list_2D[l][start_col:end_col])

    return to_append

def get_avg(nums):
    '''
    Helper function for calculating the average of a sample.
    :param nums: list of numbers
    :return: average of list
    '''
    #TODO: fill me in!
    mean = sum(nums)/len(nums)
    return mean

def get_stdev(nums):
    '''
    Helper function for calculating the standard deviation of a sample.
    :param nums: list of numbers
    :return: standard deviation of list
    '''
    #TODO: fill me in!
    mean = get_avg(nums)
    std = (sum(((x-mean)**2) for x in nums)/(len(nums)-1)) **0.5
    return std

def get_standard_error(a, b):
    '''
    Helper function for calculating the standard error, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: standard error of a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    std_a = get_stdev(a)
    std_b = get_stdev(b)
    ste = ((std_a ** 2) / len(a) + (std_b ** 2) / len(b))**0.5
    return ste

def get_2_sample_df(a, b):
    '''
    Calculates the combined degrees of freedom between two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: integer representing the degrees of freedom between a and b (see studio 6 guide for this equation!)
    HINT: you can use Math.round() to help you round!
    '''
    #TODO: fill me in!
    se = get_standard_error(a, b)
    std_a = get_stdev(a)
    std_b = get_stdev(b)
    na = len(a)
    nb = len(b)
    df_2 = round(se**4/((std_a**2/na)**2/(na-1) + (std_b**2/nb)**2/(nb-1)))
    return df_2

def get_t_score(a, b):
    '''
    Calculates the t-score, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: number representing the t-score given lists a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    t_score = (get_avg(a) - get_avg(b))/ get_standard_error(a, b)
    if t_score < 0:
        return t_score
    else:
        return -1*t_score

def perform_2_sample_t_test(a, b):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates a p-value by performing a 2-sample t-test, given two lists of numbers.
    :param a: list of numbers
    :param b: list of numbers
    :return: calculated p-value
    HINT: the t_dist.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    return t_dist.cdf(get_t_score(a, b),get_2_sample_df(a, b))


# [OPTIONAL] Some helper functions that might be helpful in get_expected_grid().
# def row_sum(observed_grid, ele_row):
# def col_sum(observed_grid, ele_col):
# def total_sum(observed_grid):
# def calculate_expected(row_sum, col_sum, tot_sum):

def get_expected_grid(observed_grid):
    '''
    Calculates the expected counts, given the observed counts.
    ** DO NOT modify the parameter, observed_grid. **
    :param observed_grid: 2D list of observed counts
    :return: 2D list of expected counts
    HINT: To clean up this calculation, consider filling in the optional helper functions below!
    '''
    #TODO: fill me in!
    rows = len(observed_grid)
    cols = len(observed_grid[0])
    row_total = [sum(observed_grid[i]) for i in range(rows)]
    col_total = [sum([col[j] for col in observed_grid]) for j in range(cols)]
    grand_total = sum(row_total)
    expected_grid = [[0] * cols for i in range(rows)]
    for m in range(rows):
        for n in range(cols):
            expected_grid[m][n] = row_total[m] * col_total[n] / grand_total
    return expected_grid

def df_chi2(observed_grid):
    '''
    Calculates the degrees of freedom of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: degrees of freedom of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    rows = len(observed_grid)
    cols = len(observed_grid[0])
    df_c = (rows-1) * (cols-1)
    return df_c

def chi2_value(observed_grid):
    '''
    Calculates the chi^2 value of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: associated chi^2 value of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    rows = len(observed_grid)
    cols = len(observed_grid[0])
    chi2value = 0
    expected_grid = get_expected_grid(observed_grid)
    for i in range(rows):
        for j in range(cols):
            chi2value += ((observed_grid[i][j] - expected_grid[i][j]) **2) / expected_grid[i][j]
    return chi2value

def perform_chi2_homogeneity_test(observed_grid):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates the p-value by performing a chi^2 test, given a list of observed counts
    :param observed_grid: 2D list of observed counts
    :return: calculated p-value
    HINT: the chi2.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    chi2value = chi2_value(observed_grid)
    df_c = df_chi2(observed_grid)
    p_value = 1-chi2.cdf(chi2value, df_c)
    return p_value

# These commented out lines are for testing your main functions. 
# Please uncomment them when finished with your implementation and confirm you get the same values :)
def data_to_num_list(s):
  '''
    Takes a copy and pasted row/col from a spreadsheet and produces a usable list of nums. 
    This will be useful when you need to run your tests on your cleaned log data!
    :param str: string holding data
    :return: the spliced list of numbers
    '''
  return list(map(float, s.split()))

"""
# t_test:
alog_t_list = data_to_num_list(alog) 
blog_t_list = data_to_num_list(blog)
print(get_t_score(alog_t_list, blog_t_list))
print(perform_2_sample_t_test(alog_t_list, blog_t_list))


# chi2_test:
alog_c2_list = data_to_num_list(alog_count) 
blog_c2_list = data_to_num_list(blog_count)
c1_observed_grid = [alog_c2_list, blog_c2_list]
print(chi2_value(c1_observed_grid))
print(perform_chi2_homogeneity_test(c1_observed_grid))

"""
