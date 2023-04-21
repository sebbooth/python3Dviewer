import fileinput

def readFile(fileName):
    vertices = []
    polygons = []

    for f in fileinput.input(fileName):
        if f[0:2] == 'v ':
            vertex = f.split(" ")[1:]
            vertex = [float(n) for n in vertex]
            vertices.append(vertex)

        elif f[0] == 'f':
            poly = f.split(" ")[1:]
            poly = [int(p.split("/")[0]) for p in poly]
            polygons.append(poly)

    print("Vertices")
    for v in vertices:
        print(v)

    print("Polys")
    for p in polygons:
        print(p)        

    return vertices, polygons