systems = ("rdb", "fdb", "kvell", "kvell1")
workloads = ("get", "set")

for s in systems:
    for w in workloads:
        c = 0
        t = 0
        name = "-".join([s, "latency", w, "udb"])
        with open(name, "r") as f:
            for l in f.readlines():
                a = l.strip().split()
                c += int(a[2])
                t += int(a[0]) * int(a[2])

        print(t/c, s, w)
