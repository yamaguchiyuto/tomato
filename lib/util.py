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
