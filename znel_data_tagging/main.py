import pickle
import os
import time

import xlsxwriter
from aip import AipNlp

import conf

def get_sim(client, text1, text2):
    """
    :param client: The client of AipNlp
    :param max_trials: The maximum number of trials to get sim from Baidu server
    :return: Similarity between text1 and text2
    """
    got_sim = False
    trials = 0
    while got_sim == False and trials < conf.max_trials:
        response = {'score': -1}

        try:
            response = client.simnet(text1, text2)
        except Exception as e:
            print(f'[ERROR] {e}')
        
        got_sim = 'score' in response
        trials += 1
    return response.get('score', -1)

def get_data_in_row(client, phrase, dst):
    """
    :param phrase: The phrase to be analyzed
    :param dst: The destination sectors of industry
    :return: the maximum similarity, and the conf.candi maximum dst sectors which are similar to phrase
    """
    sims = [[-1, sector] for sector in dst]

    for i, d in enumerate(dst):
        sims[i][0] = get_sim(client, phrase, d)
        print(f'[NORMAL] Calculated similarity with sector No.{i+1}')

    sims = sorted(sims, reverse=True)
    candidates = [d[1] for d in sims[:conf.candi]]
    return sims[0][0], candidates

def get_data(client, src, dst):
    """
    :param src: The source phrases
    :param dst: The destination sectors of industry
    :param st: The start phrase
    :param rg: The range of phrases
    :return: 2-layer nested array
    """
    data = []
    header = ['No', 'Ind', 'Max Similarity'] + [f'Candidate {i}' for i in range(1, conf.candi+1)]  # 3 + conf.candi rows in total
    data.append(header)

    st_time = time.time()

    for i in range(conf.count):
        phrase = src[conf.start-1+i]
        max_sim, candidates = get_data_in_row(client, phrase, dst)
        row = [conf.start + i, phrase, max_sim] + candidates
        data.append(row)

        now = time.time()
        print(f'[NORMAL] Phrase No.{conf.start+i} finished, {i+1} phrases finished in total')
        print(f'[NORMAL] Result of phrase No.{conf.start+i}: {row}')
        print(f'[NORMAL] Average Speed: {(now-st_time)/(i+1)} seconds per phrase')
        print(f'[NORMAL] Time consumed: {now-st_time} seconds in total')
    return data

def save_words_to_xlsx(data, filename, x=1, y=1):
    """
    :param data: The data to be saved
    :param filename: The filename of the data
    :param x: Data will be saved at row x
    :param y: Data will be saved at column y
    save words to an xlsx file
    """
    # If file already exists, delete it.
    if os.path.exists(filename):
        os.remove(filename)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Write Data to worksheet
    x -= 1
    y -= 1
    for i, row in enumerate(data):
        for j, word in enumerate(row):
            worksheet.write(x+i, y+j, word)

    workbook.close()

if __name__ == "__main__":
    with open(r'src.txt', 'r', encoding='utf-8') as f:
        src_words = f.readlines()
        src_words = [w.strip() for w in src_words]
    with open(r'dst.txt', 'r', encoding='utf-8') as f:
        dst_words = f.readlines()
        dst_words = [w.strip() for w in dst_words]

    # client = object
    client = AipNlp(conf.APP_ID, conf.API_KEY, conf.SECRET_KEY)

    data = get_data(client, src_words, dst_words)

    # Save the data to data.pkl
    try:
        with open(f'Result (from {conf.start} to {conf.start+conf.count-1}).pkl', 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f'[ERROR] {e}')

    # Save the data to data.xlsx
    try:
        save_words_to_xlsx(data, f'Result (from {conf.start} to {conf.start+conf.count-1}).xlsx')
    except Exception as e:
        print(f'[ERROR] {e}')
    
    print('[NORMAL] Succeed!')

    # read data.pkl
    # with open('data.pkl', 'rb') as f:
    #     data = pickle.load(f)