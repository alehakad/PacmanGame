def h(start, end):  # эвристика - расстояние мнк
    return min(abs(start[0] - end[0]) + abs(start[1] - end[1]), 1000 - abs(start[0] - end[0]) + abs(start[1] - end[1]),
               abs(start[0] - end[0]) + 680 - abs(start[1] - end[1]))


def a(start, end, graph):
    n = len(graph)
    closed = []  # рассмотренные вершины
    openl = [start]  # текущие вершины
    froml = {x: n for x in graph.keys()}
    g = {x: n ** 2 for x in graph.keys()}
    f = {x: n ** 2 for x in graph.keys()}
    g[start] = 0
    for v in graph[start]:
        g[v] = 1
    f[start] = h(start, end)
    while openl != []:
        curr = minf(openl, f)
        # print(curr)
        if curr == end:
            return decode(froml, start, end)
        openl.remove(curr)
        closed.append(curr)
        for neig in graph[curr]:
            if not (neig in closed):
                temp_g = g[curr] + 1
                if not (neig in openl) or temp_g < g[neig]:
                    froml[neig] = curr
                    g[neig] = temp_g
                    f[neig] = g[neig] + h(neig, end)
                if not (neig in openl):
                    openl.append(neig)
    return False


def minf(openl, f):  # минимальный элемент из текущих по f
    minel = openl[0]
    for i in openl:
        if f[i] <= f[minel]:
            minel = i
    return minel


def decode(froml, start, end):
    res = []
    i = end
    while i != start:
        res.insert(0, i)
        i = froml[i]
    return (res)
