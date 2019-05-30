entities_file = "queries_detailes.xml"
entities_data = []
this_query = {}
save_counter_picke = "counter_of_entities.pickle"
information = ["<name>", "<enttype>", "<docid>", "<beg>", "<end>"]
i = 0
import pickle
import pickle
import numpy as np


def save_to_file(var, file):
    out_file = open(file, "wb")
    pickle.dump(var, out_file)
    out_file.close()


def load_from_file(file):
    in_file = open(file, "rb")
    var = pickle.load(in_file)
    in_file.close()
    return var


def scan_file_line_by_line(doc_filename, doc_name, entities, data_on_entity, c):
    with open(doc_filename) as f:
        for i, line in enumerate(f):
            line = line.strip()
            for e in entities:
                if e in line:
                    c[e] += 1
                    requested_data = (doc_name, i + 1, line)
                    data_on_entity[e] = data_on_entity.get(e, [])
                    data_on_entity[e].append(requested_data)


def make_command(cmd):
    import subprocess
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    out = str(stdout)[2:-1]
    return out

def scan_file_grep(doc_filename, doc_name, entities, data_on_entity, c):
    import subprocess
    # with open('query.txt', 'r') as f:
    import re
    for e in entities:
        cmd = ["grep", "-inr", "-A 5", "-B 5",e, doc_filename]
        grep_rs = make_command(cmd)
        if len(grep_rs) > 0:
            print(grep_rs)
            text = grep_rs.replace(doc_filename,'')
            sentences = text.replace("\n","\\n").split("\\n")[:-1]
            if(len(sentences)%11!=0):
                print(sentences)
            # if any(map(lambda x: len(x.replace("</P>","").replace("<P>",""))<=3,sentences)):
            #     print(doc_filename)
            #     print(sentences)



def process_data():
    with open(entities_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("<query id="):
                this_query = {}
                this_query["id"] = line[line.find('"') + 1:line.rfind('"')]
                i = 0
                continue
            try:
                info = information[i]
                if line.startswith(info):
                    this_name = line[line.find(info) + len(info):line.rfind("</")]
                    this_query[info[1:-1]] = this_name
                    i += 1
            except:
                if line.startswith("</query>"):
                    if len(this_query) == len(information) + 1:
                        entities_data.append(this_query)

    print(len(entities_data))
    all_entities = set(map(lambda x: x["name"], entities_data))
    data_on_entity = {}
    import os
    from collections import Counter
    c = Counter()
    documents_dir = "2014_source_doc_set"
    for doc_name in os.listdir(documents_dir):
        doc_filename = os.path.join(documents_dir, doc_name)
        scan_file_line_by_line(doc_filename, doc_name, all_entities, data_on_entity, c)
        scan_file_grep(doc_filename, doc_name, all_entities, data_on_entity, c)

    print(c)
    save_to_file([data_on_entity, c], save_counter_picke)


if __name__ == '__main__':
    process_data()
    data_on_entity, c = load_from_file(save_counter_picke)
    for e, count in c.most_common():
        print(e)
        print(count)
        for line in data_on_entity[e]:
            print(line)

    print("done with data on entity")
    values = np.array(list(dict(c).values()))
    # print((c.most_common()))
    print(np.sum(values))
