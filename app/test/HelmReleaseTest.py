import sys
sys.path.append('../')
from models.K3dConfig import K3dConfig


p = K3dConfig(1, 1, "true")
result = p.create()
# return result

# p = HelmRelease(f"h1e7rl5a", "nginx-ingress", "default", "https://helm.nginx.com/stable")
# p.install()