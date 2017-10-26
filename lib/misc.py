# import sqlite3

# class DBconnector:
#     def __init__(self, db_file):
#         self.conn = sqlite3.connect(db_file)
#         self.cur = conn.cursor()

#     def

def result_dump(result_list, file):
    '''
    Dump the list into a file, separated by \n
    '''
    with open(file, 'w') as f:
        for res in result_list:
            f.write('{}\n'.format(res))