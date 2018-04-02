import matplotlib.pyplot as plt
import numpy as np

from Fluid import Fluid
from FractureNetworkThermal import FractureNetworkThermal

# fluid properties
cp_w = 4300
rho_w = 1000.0
mu_w = 1E-3

# reservoir properties
k_r = 2.9
cp_r = 1050.0
rho_r = 2700.0
alpha_r = k_r / (rho_r * cp_r)

# operational properties
m_inj = 50.0
P_inj = 0
t_end = 86400 * 365.25 * 40

# network properties
n_segs = 14
conn = [(0, 1), (1, 2), (2, 3), (1, 4), (2, 5), (3, 6),
        (4, 5), (5, 6), (4, 7), (5, 8), (6, 9), (7, 8), (8, 9), (9, 10)]
L = 250 * np.ones(n_segs)
L[0] = 100
L[-1] = 100
H = 500 * np.ones(n_segs)
A = L.sum() * H.mean()
w = 1E-3 * np.ones(n_segs)
n_inj = 0
n_prod = 10

# create network object
fluid = Fluid(density=rho_w, viscosity=mu_w, heat_capacity=cp_w)
network = FractureNetworkThermal(conn, L, H, w, k_r, alpha_r)

# calculate flow in the network
essential_bc = {n_inj: P_inj}
point_sources = {n_prod: -m_inj}
network.calculate_flow(fluid, essential_bc, point_sources, correct=False)

# calculate temperature and plot results
segs_to_plot = (0, 1, 2, 5, 10, 13)
t = t_end * np.linspace(1.0 / 100, 1, num=100)
tau = k_r * rho_r * cp_r / (cp_w * m_inj / A)**2
Theta = np.zeros((len(segs_to_plot), len(t)))
f = plt.figure()

for i, seg in enumerate(segs_to_plot):
    z = np.array([L[seg]])
    Theta[i, :] = network.calculate_temperature(fluid, seg, z, t).ravel()
    plt.plot(t / tau, Theta[i, :], '--')

plt.ylim((0, 1))
plt.xlim((0, 3))
plt.ylabel('$\Theta$ (-)')
plt.xlabel('$\tau$ (-)')
f.show()
