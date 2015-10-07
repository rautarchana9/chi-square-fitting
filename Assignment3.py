from math import exp
from math import sqrt
import numpy as np
import pylab as pl
Y_fn = []
Time = []
def read_data(file_name):
    T = []
    Y = []
    with open(file_name, "rb") as f:
        for line in f:
            #print line
            (tvalue, yvalue) = line.split(',')
            T.append(float(tvalue))
            Y.append(float(yvalue))
    return (T, Y)

def chi_squared(a, t1, t2):
    global Time
    global Y_tilde
    global Y_fn
    x = len(Time)
    chi_sq = 0
    y = [a*exp(-Time[i]/t1) + (10000-a)*exp(-Time[i]/t2) for i in range(x)]
    Y_fn = y
    #print "y Y_tilde chi_sq"
    for i in range(x):
        term = (y[i] - Y_tilde[i])*(y[i] - Y_tilde[i])/Y_tilde[i]
        chi_sq += term
        
        #print Time[i], y[i], Y_tilde[i], chi_sq

    return chi_sq

def chi_squared_for_a(a):
    return chi_squared(a, t1, t2)

def chi_squared_for_t1(t1):
    return chi_squared(a, t1, t2)

def chi_squared_for_t2(t2):
    return chi_squared(a, t1, t2)


au = (sqrt(5) - 1)/2

def find_minimum(f, precision = 0.0005): 

    low = precision
    f_low = f(low)
    high = 2.0 * low
    f_high = f(high)
    while f_high < f_low:
        high = 2.0 * high
        f_high = f(high)
   
    gap = high - low
    mid_low = low + gap * au * au
    f_mid_low = f(mid_low)
    mid_high = low + gap * au
    f_mid_high = f(mid_high)

    while gap > precision:
        if f_mid_low < f_mid_high:
           (high, f_high) = (mid_high, f_mid_high)
           gap = high - low
           (mid_high, f_mid_high) = (mid_low, f_mid_low)
           mid_low = low + gap * au * au
           f_mid_low = f(mid_low)
        else:
           (low, f_low) = (mid_low, f_mid_low)
           gap = high - low
           (mid_low, f_mid_low) = (mid_high, f_mid_high)
           mid_high = low + gap * au
           f_mid_high = f(mid_high)
    solution = (low + high)/2.0
    return  (solution, f(solution))

print
print "AIM OF THE PROGRAM"
print
print "To optimize the values of a, t1 and t2 in the following function so as to fit the given data with this function,"
print "where the best fit is decided by the value of a parameter called chi-square.\n"
print "y(t) = a.exp(-t1/t) + (10000-a).exp(-t2/t)"
print

(Time, Y_tilde) = read_data("Project3Data.csv")

pl.plot(Time, Y_tilde, "r")
pl.title("Double exponential decay of fluorescence intensity (actual)")
pl.xlabel("Time (arbitrary units)")
pl.ylabel("Intensity (arbitrary units)")
pl.show()

(a, t1, t2, value) = (1000, 5, 5, 1000)

while (value >= 900):
    (new_a, value) = find_minimum(chi_squared_for_a)
    a = new_a
    (new_t1, value) = find_minimum(chi_squared_for_t1)
    t1 = new_t1
    (new_t2, value) = find_minimum(chi_squared_for_t2)
    t2 = new_t2
    #plot_actual = pl.plot(Time, Y_tilde, "r")
    #plot_fitted = pl.plot(Time, Y_fn, "b")
    #pl.title("Double exponential decay of fluorescence intensity (actual and fitted)")
    #pl.xlabel("Time (arbitrary units)")
    #pl.ylabel("Intensity (arbitrary units)")
    #pl.show()
    #These statements have been given hash tags intentionally because the while loop causes numerous iterations before optimizing the a, t1 and t2,
    #otherwise, at each iteration, the user will have to close the plot window, and it would take a lot of time to reach the end of the loop.
    
print "The final vaues of a, t1 and t2, respectively are:"
print "%0.2f %0.2f %0.2f"%(a, t1, t2)
print
print "The final value of chi-square after fitting the given data is:",
print "%0.2f"%chi_squared(a, t1, t2)

plot_actual = pl.plot(Time, Y_tilde, "r")
plot_fitted = pl.plot(Time, Y_fn, "b")
pl.title("Double exponential decay of fluorescence intensity (actual and fitted)")
pl.xlabel("Time (arbitrary units)")
pl.ylabel("Intensity (arbitrary units)")
#pl.legend([plot_actual, plot_fitted], ("Actual data", "Fitted data"), "best")
#The above mentioned function (pl.legend()) is giving an error in my system.

pl.show()

