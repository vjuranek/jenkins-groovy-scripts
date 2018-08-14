/**
 * For given Jenkins slaves iterates over all jobs tied to this slave and add appropriate lock (from Lock and latches plugin) if no lock is configured.
 * It's typically used when you want to enforce that job acquire specified lock before running on given slave.
 * Typically this is used to synchronize usage of some external resource which is not under Jenkins control (e.g. database etc.).
 */

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