'''
Sequential approach
'''

import time
from websites import SITE_LIST, check_website


def main():
    '''
    Main function
    '''
    start_time = time.time()
    for address in SITE_LIST:
        check_website(address)
    end_time = time.time()
    print('Time for sequential:', end_time - start_time, 'secs')


if __name__ == '__main__':
    main()
