import matplotlib.pyplot as plt
import json
from pprint import pprint

with open('rho_value.json') as f:
    data = json.loads(f.read())


rho_in = [ d[1] for d in data]
rho_out = [ d[2] for d in data]

plt.plot(rho_in)
plt.title('Rho_in pour chaque trame de la vidéo')
plt.show()
plt.plot(rho_out)
plt.title('Rho_out pour chaque trame de la vidéo')
plt.show()
pprint(rho_in)


