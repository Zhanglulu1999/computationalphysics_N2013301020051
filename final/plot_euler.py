import calc as ca

# euler;rk;emm;exact

test = ca.nuclei(10000,10,0.1)
test.exact(100)
test.euler(100)

rs = []
h = []

for i in range(1000):
    step = float((i + 1)) / 1000.
    test.step = step
    test.exact(100)
    test.euler(100)
    tot = 0
    for j in range(len(test.nu)):
        tot += (test.base[j] - test.nu[j]) * (test.base[j] - test.nu[j])
    #print tot,",",len(test.nu)
    tot = tot / float(len(test.nu))
    rs.append(tot)
    h.append(step)
    
        

ca.plt.plot(h,rs)
ca.plt.show()    
