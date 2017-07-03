import black_scholes as bs
import math
# Test
def main():
    print("UAI 2017")
    rate = .03
    vol = .12
    time_mat = 1
    strike = 100
    spot = 100
    type1 = "Call"
    type2 = "Put"

    result1 = bs.call_put_value(type1, spot, time_mat, strike, rate, vol)
    result2 = bs.call_put_value(type2, spot, time_mat, strike, rate, vol)
    F = spot*math.exp(rate*time_mat)
    df = math.exp(-rate*time_mat)
    result3 = df*(F - strike)

    print("Valor Call: " + str(result1))
    print("Valor Put: " + str(result2))
    print("Valor Call - Put: " + str(result1-result2))
    print("Valor Forward: " + str(result3))

    return


if __name__ == "__main__":
    main()