import pandas as pd
import matplotlib.pyplot as plt

def ema(N, array, day):
    """
    This function calculates the Exponential Moving Average
    """
    alpha = 2 / (N + 1)
    value = 1 - alpha
    numerator = 0
    denominator = 0

    for i in range(N):
        if day - i >= 0:
            x = value ** i
            numerator += x * array[day-i]
            denominator += x
    
    return numerator / denominator

def macd(array, day):
    """
    This function calculates the Moving Average Convergence/Divergence
    """
    ema12 = ema(12, array, day)
    ema26 = ema(26, array, day)
    return ema12 - ema26

def signal(macdvalues, day):
    return ema(9, macdvalues, day)

data = pd.read_csv('TSLA.csv')
n = len(data)

macdvalues = []
signalvalues = []

for i in range(n):
    macdvalues.append(macd(data['Value'], i))
    signalvalues.append(signal(macdvalues, i))

data['MACD'] = macdvalues
data['Signal'] = signalvalues

plt.plot(data['Data'], data['Value'], label='TSLA')
plt.plot(data['Data'], data['Signal'], label='Signal')
plt.plot(data['Data'], data['MACD'], label='MACD')
plt.title('TSLA with MACD and Signal lines')
plt.legend()
plt.xticks(data['Data'][::80])
plt.show()

capital = 1000
shares = 0

print("Initial capital:", capital)

for i in range(n):
    if macdvalues[i] > signalvalues[i] and macdvalues[i-i] < signalvalues[i-1]:
        if shares != 0:
            capital = capital + data['Value'][i]*shares
            shares = 0
    elif macdvalues[i] < signalvalues[i] and macdvalues[i-1] > signalvalues[i-1]:
        if capital > data['Value'][i]:
            shares = capital/data['Value'][i]
            capital = 0

if capital == 0:
    capital = shares*data['Value'][n-1]

print("Final capital:", capital)