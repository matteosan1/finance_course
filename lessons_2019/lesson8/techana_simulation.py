import numpy as np
import matplotlib.pyplot as plt
import json, random

def line(x, px, py, qx, qy):
    m = (py - qy)/(px - qx)
    y = m*x - (m*px - py)
    return y * (1 + np.random.standard_normal()*0.015)

def gen_paths(S0, r, sigma, T, M, I):
    dt = float(T) / M
    paths = np.zeros((M + 1, I), np.float64)
    paths[0] = S0
    for i in range(I):
        for t in range(1, M + 1):
            rand = np.random.standard_normal()
            paths[t, i] = paths[t - 1, i] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * rand)
    return paths

def head_shoulder_up(index, M, path):
    length1 = np.random.randint(10, 11)
    length2 = np.random.randint(20, 21)
    length3 = np.random.randint(10, 11)
    offset = index #np.random.randint(M - 75)
    tot_length = length1 + length2 + length3

    bottom = max(paths[offset, n], paths[offset + tot_length, n])

    diff_shoulder = np.random.randint(120, 130)
    shoulder1 = bottom * diff_shoulder / 100
    head = bottom * np.random.randint(diff_shoulder, 140) / 100
    neck = bottom * np.random.randint(115, diff_shoulder) / 100
    l1 = int(length1 * 0.5)
    l2 = int(length1 * 0.5)
    local_offset = offset
    for i in range(l1):
        path[i + local_offset] = line(i + local_offset,
                                        local_offset, path[local_offset],
                                        local_offset + l1, shoulder1)
    for i in range(l2 + 1):
        path[i + offset + l1] = line(i + local_offset + l1,
                                        local_offset + l1, shoulder1,
                                        local_offset + l1 + l2, neck)

    l1 = int(length2 * 0.5)
    l2 = int(length2 * 0.5)
    local_offset = offset + length1
    for i in range(l1):
        path[i + local_offset] = line(i + local_offset, local_offset, neck,
                                          local_offset + l1, head)
    for i in range(l2 + 1):
        path[i + local_offset + l1] = line(i + local_offset + l1,
                                              local_offset + l1, head,
                                              local_offset + l1 + l2, neck)

    l1 = int(length3 * 0.5)
    l2 = int(length3 * 0.5)
    local_offset = offset + length1 + length2
    for i in range(l1):
        path[i + local_offset] = line(i + local_offset, local_offset, neck,
                                          local_offset + l1, shoulder1)
    for i in range(l2 + 1):
        path[i + local_offset + l1] = line(i + local_offset + l1,
                                               local_offset + l1, shoulder1,
                                               local_offset + l1 + l2, path[local_offset + length3])

def triangle(index, M, path):
    offset = index#np.random.randint(M - 75)
    lengths = []
    for i in range(10):
        lengths.append(5)

    top = max(path[offset], path[offset + sum(lengths)])
    bottom = min(path[offset], path[offset + sum(lengths)])
    last_peak = top - (top - bottom) * 0.1

    for i in range(1, 10, 2):
        path[sum(lengths[:i])+offset] = top

    for i in range(2, 10, 2):
        l = sum(lengths[:i])+offset
        path[l] = line(l, offset, bottom, offset + sum(lengths), last_peak)

    local_offset = offset
    for n_l, l in enumerate(lengths):
        for i in range(l):
            path[i + local_offset] = line(i + local_offset,
                                        local_offset, path[local_offset],
                                        local_offset + l, path[local_offset+l])
        local_offset = offset + sum(lengths[:n_l])

if __name__ == "__main__":
    np.random.seed(1)
    random.seed(1)
    S0 = 100
    r = 0.01
    sigma = 0.2
    T = 1
    M = 120# int(365*T)
    N = 60
    labels = [0 for _ in range(N*M*3)]
    paths = gen_paths(S0, r, sigma, T, M, N*M*3)
    
    for n in range(N*M*3):
        
        print (n)
        curve_type = random.randint(0, 2)
        index = random.randint(0, 70)
        if curve_type == 1:
            head_shoulder_up(index, M, paths[:, n])
            labels[n] = 1
        elif curve_type == 2:
            triangle(index, M, paths[:, n])
            labels[n] = 2
        else:
            labels[n] = 0
        #for index in range(70):
        #    if n < 20:
        #        head_shoulder_up(index, M, paths[:, n*70+index])
        #        labels[n*70+index] = 1
        #    elif 20 < n < 40:
        #        triangle(index, M, paths[:, n*70+index])
        #        labels[n*70+index] = 2
            
        #if n < 10:
        #    plt.ion()
        #    plt.plot(paths[:, n:n+1])
        #    ##plt.grid(True)
        #    plt.xlabel('days')
        #    plt.ylabel('$S^{i}_{t}$')
        #    #plt.show()
        #    plt.savefig("images/image_" + str(n) + ".png")
        #    plt.close()
        
    paths = paths.transpose()
    paths = paths[:, :101].tolist()
    with open("training_techana_images.json", mode='w') as f:
        json.dump(paths, f)

    with open("training_techana_labels.json", mode='w') as f:
        json.dump(labels, f)
