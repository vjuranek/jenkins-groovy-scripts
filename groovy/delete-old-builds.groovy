/**
 * Deletes builds of the jobs older the specified number.
 */

JOB_NAME = "test"
MIN_JOB = 100

Jenkins.instance.getItem(JOB_NAME).builds.each {
  if (it.id.toInteger() < MIN_JOB) {
    println "Deleteing build " + it.id
    it.delete()
  }
}

return null