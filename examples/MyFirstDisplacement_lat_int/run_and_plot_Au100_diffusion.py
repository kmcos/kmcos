#!/usr/bin/env python
from kmcos.run import KMC_Model
import kmcos.run.acf as acf
import matplotlib.pyplot as plt
import random
import numpy as np

#Model parameters 
conc = 0.25 #Concentration of particles
Nruns = 25 #Number of trajectories to average over
Npoints = 100 #Number of points to plot from each trajectory
rerun = True #If True rerun model, if False read previous results from files
seeds = list(range(Nruns)) #Random seeds used for each trajectory

#Setting up the plot
f, (ax, ax2) = plt.subplots(1, 2, sharey=True,figsize=(6.5,4))

#Defining some parameters for each test case considering different barriers for hopping and exchange diffusion
colors = ["#cd00cd","#b64a33","#006400","b","#00FF7F"]
barriers = [[0.83,10],[0.83,0.65],[0.78,0.65],[0.73,0.65],[0.83,0.60]]
labels = [r'$\Delta E_{\mathrm{hop}}=0.83$ eV',r'$\Delta E_{\mathrm{hop}}=0.83$ eV, $\Delta E_{\mathrm{exc}}=0.65$ eV',r'$\Delta E_{\mathrm{hop}}=0.78$ eV, $\Delta E_{\mathrm{exc}}=0.65$ eV', r'$\Delta E_{\mathrm{hop}}=0.73$ eV, $\Delta E_{\mathrm{exc}}=0.65$ eV',r'$\Delta E_{\mathrm{hop}}=0.83$ eV, $\Delta E_{\mathrm{exc}}=0.60$ eV']
positions = [[37000,220],[30,450],[40,610],[26,1400],[10,1150]]

#loop over barrier values
plot_num = 0
for barrier, label, color, pos in zip(barriers,labels,colors,positions):
    MSDs = np.zeros((Nruns,Npoints))
    times = np.zeros((Nruns,Npoints))

    if rerun:
        for seed in seeds:

            #initiate model
            model = KMC_Model(print_rates=False, banner=False, random_seed=seed+1)
            model.parameters.E_hop = barrier[0]
            model.parameters.E_exc = barrier[1]

            #populate lattice
            nsites = model.size[0]*model.size[1] #Total number of sites
            Nsites = int(np.floor(float(conc)*nsites)) #Number of populated sites

            sites_list = []
            for i in range(model.size[0]):
                for j in range(model.size[1]):
                    sites_list.append([i,j])

            #random population of sites
            chosen_sites = random.sample(sites_list, Nsites)
            for elem in chosen_sites:
                model._put(site=[elem[0],elem[1],0,1], new_species=model.proclist.au)
            model._adjust_database()

            #non-random population of sites
            #for elem in sites_list[:Nsites]:
            #    model._put(site=[elem[0],elem[1],0,1], new_species=model.proclist.au)
            #model._adjust_database()

            #do relaxation
            model.do_steps(1e6)
            atoms=model.get_atoms()
            kmc_time0=atoms.kmc_time

            #initialize ac
            acf.initialize_msd(model, 'au')
            for N in range(Npoints):
                #do steps
                acf.do_kmc_steps_displacement(model, 1e5)

                #get MSD
                MSD = acf.calc_msd(model) #in Ang**2 averaged over all tracked particles
                MSDs[seed,N] = MSD

                #get kmc time
                atoms=model.get_atoms()
                time=atoms.kmc_time-kmc_time0
                times[seed,N] = time 

            model.deallocate()

        plot_times = np.average(times,axis=0)
        plot_MSDs = np.average(MSDs,axis=0)
        np.savetxt('plot_times_%d.txt'%plot_num,plot_times)
        np.savetxt('plot_MSDs_%d.txt'%plot_num,plot_MSDs)

    else:
        plot_times = np.loadtxt('plot_times_%d.txt'%plot_num)
        plot_MSDs = np.loadtxt('plot_MSDs_%d.txt'%plot_num)

    plot_times = np.hstack((np.array([0]),plot_times))
    plot_MSDs = np.hstack((np.array([0]),plot_MSDs))*0.01
    ax.plot(plot_times,plot_MSDs,color=color)
    ax2.plot(plot_times,plot_MSDs,color=color,label=label)
    params=np.polyfit(plot_times,plot_MSDs,1)
    slope = params[0]
    dim = 2 #dimensionality of lattice
    D = slope/(2*dim)
    if label == r'$\Delta E_{\mathrm{hop}}=0.83$ eV':
        ax2.text(pos[0],pos[1],r'D=%.4f nm$^2$/ s'%(D*1),color=color)
    elif label == r'$\Delta E_{\mathrm{hop}}=0.83$ eV, $\Delta E_{\mathrm{exc}}=0.60$ eV':
        ax.text(pos[0],pos[1],r'D=%.0f nm$^2$/ s'%(D*1),color=color)
    else:
        ax.text(pos[0],pos[1],r'D=%.1f nm$^2$/ s'%(D*1),color=color)
    print('Conc: %.1f, Ehop: %.2f, Eexc: %.2f, D: %.3f' %(conc,barrier[0],barrier[1],D))
    plot_num += 1

#print MSDs
#print times

f.text(0.5, 0.01, 'time (s)', ha='center')
ax.set_xlim(0, 90)
ax2.set_xlim(10000, 100000)

ax.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax.yaxis.tick_left()
ax2.yaxis.tick_right()
ax2.tick_params(labelright='off')  # don't put tick labels at the right
ax.set_xticks([0,20,40,60,80])
ax2.set_xticks([50000,100000])

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((1-d, 1+d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1-d, 1+d), (1-d, 1+d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (-d, +d), **kwargs)  # bottom-left diagonal
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

ax.set_ylim(0, 1700)
ax.set_ylabel(r'Mean squared displacement (nm$^2$)')
ax2.legend(fontsize=12, loc = "upper right")
plt.subplots_adjust(left=0.12, bottom=0.115, right=0.94, top=0.97,
                wspace=0.05)
plt.savefig('MSD_Au_diffusion.eps')

