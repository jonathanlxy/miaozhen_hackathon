def result_dump(result_list, file):
    '''
    Dump the list into a file, separated by \n
    '''
    with open(file, 'w') as f:
        for res in result_list:
            f.write('{}\n'.format(res))