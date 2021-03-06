import matplotlib.pyplot as plt
import numpy as np
import math


class shell:
    y = []
    x = []
    vx = []
    vy = []
    t = 0
    v = 0
    vt = 0
    theta = 0
    degree = 0
    g = 0.0098
    maxx = 0
    maxy = 0
    figure = plt.plotting()

    def __init__(self,v,theta,t):
        self.x = []
        self.y = []
        self.vx = []
        self.vy = []
        self.x.append(0)
        self.y.append(0)
        self.vx.append(v * math.cos(theta))
        self.vy.append(v * math.sin(theta))
        self.v = v
        self.theta = theta
        self.degree = theta * 180 / np.pi
        self.t = t

    def step_calc(self,step):
        self.x.append(self.x[-1] + self.vx[-1] * step)
        self.vx.append(self.vx[-1])
        self.y.append(self.y[-1] + self.vy[-1] * step)
        self.vy.append(self.vy[-1] - self.g * step)
        return self.y[-1] + self.vy[-1] * step

    def trajectory_calc(self,step):
        self.tra = 1
    	self.__init__(self.v,self.theta,self.t)
        while self.step_calc(step) > 0:
            continue

    def draw_figure(self):
        if self.tra == 1:
            lab = '$\\theta$=%6.2f$^{\circ}$,no correction' %self.degree
            line = 'solid'
        elif self.tra == 2:
            lab = '$\\theta$=%6.2f$^{\circ}$,drag correction' %self.degree
            line = 'dashed'
        else:
            lab = '$\\theta$=%6.2f$^{\circ}$,density correction' %self.degree
            line = 'dashdot'
        plt.plot(self.x,self.y,lw = 1,label = r'%s' %lab,ls = '%s' %line)
        self.maxx = max(max(self.x),self.maxx)
        self.maxy = max(max(self.y),self.maxy)

    def show_figure(self):
        self.maxx *= 1.2
        self.maxy *= 1.2
        plt.xlim(0,self.maxx)
        plt.ylim(0,self.maxy)
        plt.xticks(np.linspace(0,self.maxx,8))
        plt.yticks(np.linspace(0,self.maxy,10))
        plt.title(r"Trajectory of a cannon shell,T = %sK" %self.t)
        plt.xlabel('x(km)')
        plt.ylabel('y(km)')
        plt.legend(loc = 'upper right',fontsize = 'x-small')
        plt.minorticks_on()
        plt.grid()

        plt.show()

    def set_theta(self,tmp):
        self.theta = tmp
        self.degree = tmp * 180 / np.pi
        
    def set_theta_degree(self,tmp):
    	self.degree = tmp
    	self.theta = tmp * np.pi / 180

    def set_v(self,tmp):
        self.v = tmp
        
    def set_t(self,tmp):
        self.t = tmp

    def drag_calc(self,step):
        self.vx[-1] -= 0.04 * self.vt * self.vx[-2] * step
        self.vy[-1] -= 0.04 * self.vt * self.vy[-2] * step
        self.vt = np.sqrt(self.vx[-1] ** 2 + self.vy[-1] ** 2)
        
    def trajectory_calc_drag(self,step):
    	self.__init__(self.v,self.theta,self.t)
        self.tra = 2
        self.vt = self.v
        while self.step_calc(step) > 0:
            self.drag_calc(step)
	
    def density_calc(self,step):
        tmp = (1 - 6.5 * self.y[-2] / self.t) ** 2.5
        self.vx[-1] -= 0.04 * self.vt * self.vx[-2] * step * tmp
        self.vy[-1] -= 0.04 * self.vt * self.vy[-2] * step * tmp
        self.vt = np.sqrt(self.vx[-1] ** 2 + self.vy[-1] ** 2)
        
    def trajectory_calc_density(self,step):
        self.__init__(self.v,self.theta,self.t)
        self.tra = 3
        self.vt = self.v
        while self.step_calc(step) > 0:
            self.density_calc(step)        

class shell_firing(shell):
    def trajectory_calc_altitude(self,step,altitude):
        self.__init__(self.v,self.theta,self.t)
        self.tra = 3
        self.vt = self.v
        while self.step_calc(step) > altitude or self.vy[-1] > 0:
            self.drag_calc(step)
            continue
        return self.x[-1]

    def find_theta(self,altitude):
        deg = 0.0
        xmax = -1
        degmax = 0
        while True:
            self.set_theta_degree(deg)
            tmp = self.trajectory_calc_altitude(0.01,altitude)
            print deg,',',tmp
            if tmp > xmax:
                degmax = deg
                xmax = tmp
                deg += 0.01
            else:
                break
        xmax = -1

        while True:
            self.set_theta_degree(deg)
            tmp = self.trajectory_calc_altitude(0.01,altitude)
            print deg,',',tmp
            if tmp > xmax:
                degmax = deg
                xmax = tmp
                deg -= 0.01
            else:
                break
        return deg            

