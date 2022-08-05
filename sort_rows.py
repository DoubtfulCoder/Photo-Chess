import numpy as np

xs = np.array([1,2,1,3,5,1,4,  14,13,10,11,10,11,12])
ys = np.array([50,60,30,70,30,40,10,  140,110,110,100,130,150,120])

def sort_coords_into_rows(xs, ys):
    start_row_index = 0
    abs_value_for_approx_equal = 10

    final_xs = []
    final_ys = []

    for i in range(1, len(xs)):
        # check if x is approximately the same as the previous x 
        # meaning they are in the same row
        x = xs[i]
        if abs(x - xs[i-1]) > abs_value_for_approx_equal or i == len(xs)-1:
            # not in the same row
            end_row_index = i-1 if i != len(xs)-1 else i
            # sort the y values in the row
            # get indices of sorted y values
            sorted_indices = ys[start_row_index:end_row_index+1].argsort()
            # assign sorted indices to y values and corresponding x values
            ys[start_row_index:end_row_index+1] = ys[start_row_index:end_row_index+1][sorted_indices]
            xs[start_row_index:end_row_index+1] = xs[start_row_index:end_row_index+1][sorted_indices]

            # add the row to the final xs and ys
            final_xs.append(xs[start_row_index:end_row_index+1].tolist())
            final_ys.append(ys[start_row_index:end_row_index+1].tolist())
            
            # start new row
            start_row_index = i 

    print(xs)
    print(ys)    
    return [final_ys, final_xs]

