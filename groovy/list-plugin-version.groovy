jenkins.model.Jenkins.instance.pluginManager.plugins.each {
  println "${it} \t\t ${it.getVersionNumber()}"
}
return null