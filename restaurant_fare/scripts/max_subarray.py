input = [1,2,4,1,7,-3,2,-4,5,6,8,9,12,-7,6,5,8,9,12]

max_sum = 0
index = -1
max_sub_array = []
prev_start_index = 0
prev_end_index = -1
prev_max_sum = 0
new_sub_list_traverse = True

for val in input:
    # increment index
    index = index + 1
    if val >=0:
        # if traversing new sub list
        if new_sub_list_traverse:
            # if prev_start_index == -1:
            #     prev_start_index = index
            new_sub_list_traverse = False
        
        prev_max_sum = prev_max_sum + val
        max_sub_array.append(val)
    else:
        
        max_sub_array = []
        new_sub_list_traverse = True
        if max_sum <= prev_max_sum:
            max_sum = prev_max_sum
            prev_end_index = index - 1
        else:
            prev_start_index = index + 1
        prev_max_sum = 0

#print "prev start index", prev_start_index, "---prev end index", prev_end_index, "--length=", len(max_sub_array)
if prev_max_sum == max_sum:
    if len(max_sub_array) > (prev_end_index - prev_start_index + 1):
        print max_sub_array
    elif len(max_sub_array) == (prev_end_index - prev_start_index + 1):
        print input[prev_start_index:prev_end_index+1]
else:
    print max_sub_array