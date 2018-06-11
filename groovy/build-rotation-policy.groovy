import jenkins.model.Jenkins
import hudson.tasks.LogRotator

def DAYS_TO_KEEP = -1
def BUILDS_TO_KEEP = 10
def whiteList = []

Jenkins.instance.items.each { project ->
  println "Checking $project.displayName"

  if (project.displayName in whiteList) {
    println "\tOn white list, skipping"
    return
  }
  
  def logRotator = project.logRotator

  if(logRotator == null) {
    println "\tRetention policy is not set, setting it to default values."
    logRotator = new LogRotator(DAYS_TO_KEEP, BUILDS_TO_KEEP);
    try {
      project.setLogRotator(logRotator)
    } catch (Exception e) {
      println "\tFailed to set log rotator, check manually what's wrong!"
    }
  } else if(logRotator.numToKeep < 0 || logRotator.numToKeep > BUILDS_TO_KEEP) {
    println "\tPolicy set to ${logRotator.numToKeep}, setting default values."
    logRotator = new LogRotator(logRotator.daysToKeep, BUILDS_TO_KEEP);
    project.setLogRotator(logRotator)
  } else {
    println "\tOK"
  }
}

return null