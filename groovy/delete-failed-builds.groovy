JOB_NAME = "infinispan-spark"

Jenkins.instance.getItem(JOB_NAME).builds.each {
  if(hudson.model.Result.FAILURE == it.getResult()){
    println "Deleteing build " + it
    it.delete()
  }
}

return null