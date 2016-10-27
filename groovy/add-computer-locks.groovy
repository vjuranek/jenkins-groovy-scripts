import jenkins.model.Jenkins
import hudson.tasks.BuildWrappers
import hudson.Util
import hudson.plugins.locksandlatches.LockWrapper

def addComputerLock(computerName, lockName) {
  lc = LockWrapper.DESCRIPTOR.locks.grep({lc -> lc.name.equals(lockName)})
  Jenkins.instance.getComputer(computerName).tiedJobs.each {
    if (BuildWrappers.getFor(it).contains(LockWrapper.DESCRIPTOR)) {  //eligible to use locks plugin
      if (Util.filter(it.resourceActivities, LockWrapper.class).size() == 0) { // but not configured
        it.buildWrappersList.add(new LockWrapper(lc))
        it.save()
        println it.name
      }
    }
  }
}

addComputerLock("perf01","perf01")

return null