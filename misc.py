def write_dict_to_file_sorted_by_keys(filename, dic):
    file = open(filename, "w")
    for key in sorted(dic):
        file.write(key + " : " + str(dic[key]) + "\n")
    file.close()