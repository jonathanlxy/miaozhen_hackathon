import json

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
        json.dump(result_list, f)

def manual_rate(stdout_info, allow_sp=False):
    # Print the stdout_info to screen for manual rating
    # 0 = no good (0), 1 = good (100), 5 = not sure (50)
    m_rate = None
    # If allow sp: "?" will be decode as -99 for special action
    if allow_sp:
        score_dict = {'0': 0, '1': 100, '5': 50, '?': -99}
    else:
        score_dict = {'0': 0, '1': 100, '5': 50}
    while m_rate not in score_dict:
        print(stdout_info)
        m_rate = input('Rate ==> ')
        if m_rate in score_dict:
            return score_dict[m_rate]
        else:
            print('!!! Invalid score !!!')