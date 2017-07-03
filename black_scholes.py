import scipy.stats as st
import math

def call_put_value(type, spot, time_mat, strike, rate, vol):
    if type.lower() == "call":
        flag = 1
    else:
        flag = -1

    d1 = math.log(spot/strike) + (rate + .5*vol**2)*time_mat
    d1 /= vol*math.sqrt(time_mat)
    d2 = d1 - vol*math.sqrt(time_mat)

    N = st.norm(0, 1)
    F = spot*math.exp(rate*time_mat)
    df = math.exp(-rate*time_mat)
    return flag*df*(F*N.cdf(flag*d1)-strike*N.cdf(flag*d2))

