import subprocess
    
class HelmRelease:

  def __init__(self, k3dr_instance, release, namespace, repo):
    self.release = release
    self.k3dr_instance = "k3d-"+k3dr_instance
    self.namespace = namespace
    self.repo = repo
  
  def install(self):
    subprocess.run(["kubectl", "config", "use-context", f"{self.k3dr_instance}"])
    subprocess.run(["helm", "repo", "add", f"{self.release}", f"{self.repo}"])
    subprocess.run(["helm", "install", f"{self.release}", f"{self.release}/{self.release}"])
    