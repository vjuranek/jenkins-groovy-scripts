import jenkins.model.Jenkins

Jenkins.instance.items.each { project ->
  try {
    println "Rotating ${project.displayName}"
    project.logRotate()
  } catch (Exception e) {
    println e
  }
}

return null