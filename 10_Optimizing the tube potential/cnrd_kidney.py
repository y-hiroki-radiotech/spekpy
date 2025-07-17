from numpy import argmax # Import stuff from numpy
import matplotlib.pyplot as plt # Import pyplot for plotting
from metrics import get_metrics # See this function for details of calculation

print('\nStarting CNRD caluclations ... this may take some time!\n')
print('Kidney versus adipose\n')

## Specify modelling parameters
physics = 'casim' # Physics model (set to 'kqp' to reproduce book plots)
matd = 'Cesium Iodide' # Detector scintillator material
# <-- try changing matd to 'Gadolinium Oxysulfide' to see how things change
td = 0.03 # Scintillator thickness [cm]
rhod = 4.51 # Scintillator density [g/cm3]
f = 0.85 # Fill factor for scintillator
w = 0.01 # Pixel size [cm]
G = 0.5 # Anti-scatter grid factor (proportion of primary transmitted)

## Specify scenario parameters
kV_inc = 5. # Increment for tube potential (set to 1.0 in the book) [kV]
SDD = 100. # Source-to-detector distance [cm]
SOD = 90. # Source-to-object distance [cm]
org_thick = 1. # Organ thickness [cm]

## Specify relevant tissues
tissue1 = 'Tissue, Soft Four Component (ICRU)'
tissue2 = 'Adipose Tissue (ICRU)'
tissue3 = 'Kidney (ICRU)'

## Calculations for 15 cm thick patient
pat_thick = 15. # Patient thickness [cm]
Bg15= {tissue1: pat_thick-org_thick, tissue2: org_thick} # Background
Sg15 = {tissue1: pat_thick-org_thick, tissue3: org_thick} # Signal
kV_set,contrast15,cnr15,ki15,cnrd15 = get_metrics(Bg15,Sg15,SDD,SOD,kV_inc,
                                                 physics,matd,td,rhod,f,w,G)
i15=argmax(cnrd15) # index for maximum CNRD calue
print('CNRD is max at',kV_set[i15],'kV for patient thickness of',
      pat_thick,'cm')

## Calculations for 20 cm thick patient
pat_thick = 20. # Patient thickness [cm]
Bg20= {tissue1: pat_thick-org_thick, tissue2: org_thick} # Background
Sg20 = {tissue1: pat_thick-org_thick, tissue3: org_thick} # Signal
kV_set,contrast20,cnr20,ki20,cnrd20 = get_metrics(Bg20,Sg20,SDD,SOD,kV_inc,
                                                 physics,matd,td,rhod,f,w,G)
i20=argmax(cnrd20) # index for maximum CNRD calue
print('CNRD is max at',kV_set[i20],'kV for patient thickness of',
      pat_thick,'cm')

## Calculations for 25 cm thick patient
pat_thick = 25. # Patient thickness [cm]
Bg25= {tissue1: pat_thick-org_thick, tissue2: org_thick} # Background
Sg25 = {tissue1: pat_thick-org_thick, tissue3: org_thick} # Signal
kV_set,contrast25,cnr25,ki25,cnrd25 = get_metrics(Bg25,Sg25,SDD,SOD,kV_inc,
                                                 physics,matd,td,rhod,f,w,G)
i25=argmax(cnrd25) # index for maximum CNRD calue
print('CNRD is max at',kV_set[i25],'kV for patient thickness of',
      pat_thick,'cm')

## Plot the results
# Plot of contrast against kV
fig1, (ax1) = plt.subplots(nrows=1,ncols=1,num='1')
ax1.plot(kV_set,contrast15,'0.0',label='15 cm')
ax1.plot(kV_set,contrast20,'0.35',linestyle='dashed',label='20 cm')
ax1.plot(kV_set,contrast25,'0.7',label='25 cm')
ax1.legend(frameon=False,fontsize=12,loc='upper right')
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.set_xlim((50.,150.))
ax1.set_ylim((0.,0.06))
ax1.set_ylabel('Contrast, $C$',fontsize=12)
ax1.set_xlabel('Tube potential  [kV]',fontsize=12)
ax1.set_title('Kidney $versus$ adipose')
# Plot of noise against kV
fig2, (ax2) = plt.subplots(nrows=1,ncols=1,num='2')
ax2.plot(kV_set,contrast15/cnr15,'0.0',label='15 cm')
ax2.plot(kV_set,contrast20/cnr20,'0.35',linestyle='dashed',label='20 cm')
ax2.plot(kV_set,contrast25/cnr25,'0.7',label='25 cm')
ax2.legend(frameon=False,fontsize=12,loc='upper right')
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.set_xlim((50.,150.))
ax2.set_ylim((0.,1.4))
ax2.set_ylabel('Noise, $N$',fontsize=12)
ax2.set_xlabel('Tube potential  [kV]',fontsize=12)
ax2.set_title('Kidney $versus$ adipose')
# Plot of incident air kerma against kV
fig3, (ax3) = plt.subplots(nrows=1,ncols=1,num='3')
ax3.plot(kV_set,ki15,'0.0',label='15 cm')
ax3.plot(kV_set,ki20,'0.35',linestyle='dashed',label='20 cm')
ax3.plot(kV_set,ki25,'0.7',label='25 cm')
ax3.legend(frameon=False,fontsize=12,loc='upper left')
ax3.tick_params(axis='both', which='major', labelsize=12)
ax3.set_xlim((50.,150.))
ax3.set_ylabel('Air kerma, $K_\mathrm{air}$  [$\mu$Gy] ',fontsize=12)
ax3.set_xlabel('Tube potential  [kV]',fontsize=12)
ax3.set_title('Kidney $versus$ adipose')
# Plot of CNRD against kV
fig4, (ax4) = plt.subplots(nrows=1,ncols=1,num='4')
ax4.plot(kV_set,cnrd15**2,'0.0',label='15 cm')
ax4.plot(kV_set,cnrd20**2,'0.35',linestyle='dashed',label='20 cm')
ax4.plot(kV_set,cnrd25**2,'0.7',label='25 cm')
ax4.plot(kV_set[i15],cnrd15[i15]**2,'0.0',marker='o')
ax4.plot(kV_set[i20],cnrd20[i20]**2,'0.35',marker='o')
ax4.plot(kV_set[i25],cnrd25[i25]**2,'0.7',marker='o')
ax4.legend(frameon=False,fontsize=12,loc='upper right')
ax4.tick_params(axis='both', which='major', labelsize=12)
ax4.set_xlim((50.,150.))
ax4.set_ylim((0.,0.0025))
ax4.set_ylabel('CNRD$^2$  [$\mu$Gy$^{-1}$]',fontsize=12)
ax4.set_xlabel('Tube potential  [kV]',fontsize=12)
ax4.set_title('Kidney $versus$ adipose')

# Show plots on screen
plt.show()
