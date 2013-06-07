def calc_mean(points):
    sum_lat = sum([p[0] for p in points])
    sum_longi = sum([p[1] for p in points])
    n = len(points)
    if n == 0:
        return None
    else:
        return (sum_lat/n, sum_longi/n)

def calc_medoid(points, centroid):
    min_d = 9999999999999999999999999
    medoid = None
    for p in points:
        d = util.hubeny_distance(p, centroid)
        if d < min_d:
            min_d = d
            medoid = p
    return medoid

def calc_median(points):
    latitudes = [p[0] for p in points]
    longitudes = [p[1] for p in points]
    latitudes.sort()
    longitudes.sort()
    return (latitudes[len(latitudes)/2], longitudes[len(longitudes)/2])

def calc_variance(center, points):
    n = len(points)
    err_sum = 0
    for p in points:
        err_sum += (p[0]-center[0])**2
        err_sum += (p[1]-center[1])**2
    return err_sum / (2 * (n-1))

def hubeny_distance(p, q):
    latd = rad(p[0] - q[0])
    longd = rad(p[1] - q[1])
    latm = rad(p[0] + q[0]) / 2
    a = 6377397.155
    b = 6356079.000
    e2 = 0.00667436061028297
    W = math.sqrt(1 - e2 * math.sin(latm)**2)
    M = 6334832.10663254 / W**3
    N = a / W
    d = math.sqrt((latd*M)**2 + (longd*N*math.cos(latm))**2)
    return d


