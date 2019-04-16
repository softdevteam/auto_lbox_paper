#!/usr/bin/env python2
import os, sys
import re
import json
import numpy as np
import matplotlib.pyplot as plt

pctvalid = []
pctinvalid = []
pctnovalid = []
pctnoerror = []
pctnomulti = []

mode = "all"

def collect_stats(filename, d):
    with open(filename) as f:
        print(filename)
        l = json.load(f)
        print(l)
        total   = sum([sum(x) for x in l])
        valid   = sum([x[0] for x in l])
        invalid = sum([x[1] for x in l])
        novalid = sum([x[2] for x in l])
        noerror = sum([x[3] for x in l])
        nomulti = sum([x[4] for x in l])
        d["valid"].append(  float(valid)   / total)
        d["invalid"].append(float(invalid) / total)
        d["novalid"].append(float(novalid) / total)
        d["noerror"].append(float(noerror) / total)
        d["nomulti"].append(float(nomulti) / total)
        print("  Valid insertion:      {}/{} = {:.3}%".format(  valid, total, float(valid)/total*100   if total > 0 else 0.0))
        print("  Invalid insertion:    {}/{} = {:.3}%".format(invalid, total, float(invalid)/total*100 if total > 0 else 0.0))
        print("  No insertion (Valid): {}/{} = {:.3}%".format(novalid, total, float(novalid)/total*100 if total > 0 else 0.0))
        print("  No insertion (Error): {}/{} = {:.3}%".format(noerror, total, float(noerror)/total*100 if total > 0 else 0.0))
        print("  No insertion (Multi): {}/{} = {:.3}%".format(nomulti, total, float(nomulti)/total*100 if total > 0 else 0.0))

def get_compositions(folder):
    l = []
    for _, _, files in os.walk(folder):
        for f in files:
            if f.endswith("_log.json"):
                l.append(f)
    l.sort()
    return l

def create_diagram(source):
    d = {"valid": [], "invalid": [], "novalid": [],
         "noerror": [], "nomulti": [] }
    comps = get_compositions(source)
    for c in comps:
        collect_stats("{}/{}".format(source, c), d)
    plot(d, source, comps)

def plot(data, source, comps):
    a = np.array(data["valid"])
    b = np.array(data["invalid"])
    c = np.array(data["novalid"])
    d = np.array(data["noerror"])
    e = np.array(data["nomulti"])

    ind = np.arange(len(comps))
    fig, ax = plt.subplots(figsize=(15, 4))
    if mode == "all":
        plt.bar(ind, a)
        plt.bar(ind, c, bottom=a)
        plt.bar(ind, b, bottom=a+c)
        plt.bar(ind, d, bottom=a+b+c)
        plt.bar(ind, e, bottom=a+b+c+d)
        plt.legend(["Valid insertion", "No insertion (Valid)", "Invalid insertion", "No insertion (Error)", "No insertion (Multi)"], bbox_to_anchor=(1.04,1), loc="upper left")
    else:
        plt.bar(ind, a+c)
        plt.bar(ind, b+d+e, bottom=a+c)
        plt.legend(["Valid", "Invalid"], bbox_to_anchor=(1.04,1), loc="upper left")
    #plt.xticks(ind, ('Java+PHP', 'Java+SQL', 'Java+Lua', 'Lua+PHP', 'Lua+SQL', 'Lua+Java', 'PHP+Java', 'PHP+SQL', 'PHP+Lua', 'SQL+PHP', 'SQL+Java', 'SQL+Lua'))
    labels = [c.replace("_log.json", "") for c in comps]
    plt.xticks(ind, labels)

    plt.subplots_adjust(right=0.8)
    output = re.sub(r'[\W_]+', '', source) + ".png"
    plt.savefig(output, format="png")
    plt.show()

if __name__ == "__main__":
    source = sys.argv[1]
    create_diagram(source)
