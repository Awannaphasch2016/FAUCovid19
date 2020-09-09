# == Twitter
import datetime
import pandas

x = []
for i in range(len(all_retrieved_data)):
    # for i i n range(10):
    tt = all_retrieved_data[i]["data_from_a_file"]["metadata"]["aspect"]
    dd = pandas.DataFrame(all_retrieved_data[i]["data_from_a_file"]["data"])
    tmp = []
    for i in dd["id"].tolist():
        tmp.append(tt + str(i))
    # print(tmp)
    # x.append(dd['id'])
    # print(dd.keys())
    # print(dd['date'])
    # print(datetime.datetime.fromtimestamp(dd['date'].max()), datetime.datetime.fromtimestamp(dd['date'].min()))
    # print(len(dd['id'].unique().tolist()), dd['id'].shape)
    # x.append(dd['id'].unique().tolist())
    # x.extend(dd['id'].unique().tolist())
    x.extend(tmp)
print(len(x))
print(len(set(x)))


def intersection(a, b):
    return set(x[a]).intersection(set(x[b]))


# == Reddit
tmp = {}
ALL_ASPECTS = [
    "work_from_home",
    "social_distance",
    "lockdown",
    "reopen",
    "corona",
]
for i in all_reddit_retrieved_data:
    if i["aspect"] in ALL_ASPECTS:
        # if i['id'] == 'ibxs9m':
        # print(i['aspect'])
        # tmp.setdefault(i['aspect'], []).append(i['id'])
        tmp.setdefault(i["aspect"], []).append(i)
        # tmp.append(i)
        # tmp.append(i['id'])


# print(len(tmp))


def has_no_duplicate(aspect, tmp):
    return len(tmp[aspect]) == len(set(tmp[aspect]))


import pandas as pd


def check_if_aspect_has_no_duplicate(tmp):
    def has_no_duplicate(aspect, tmp):
        tmp_df = pd.DataFrame(tmp[aspect])
        return tmp_df["id"].unique().shape[0] == tmp_df["id"].shape[0]

    for i in ALL_ASPECTS:
        # print(i)
        # if not has_no_duplicate(i, tmp):
        if not has_no_duplicate(i, tmp):
            tmp_df = pd.DataFrame(tmp[i])
            tmp_df = tmp_df.drop_duplicates(subset=["id"])
            tmp[i] = tmp_df.to_dict("record")
    return tmp


# == query
query = """create table if not exists TEST (
    id string
    ,name string
    ,unique (id, name)
    );
    """
c = self.conn.cursor()
c.execute(query)

insert = "insert into TEST (id, name) values(2, 'Anak')"
c = self.conn.cursor()
c.execute(insert)

self.conn.cursor().execute("drop table if exists TEST")

self.conn.commit()
self.conn.close()
