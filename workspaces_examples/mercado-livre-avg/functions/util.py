def calc_avg(data):
    results = data.results
    
    result_count = 0
    sum_all_prices = 0.00
    
    for result in results:
        sum_all_prices += result.price
        result_count += 1

    return "R$ {0:.2f}".format(sum_all_prices / result_count)