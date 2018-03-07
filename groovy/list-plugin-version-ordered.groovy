/**
 * List instelled plugins and versions in alpabetical order
 */

plugins = new TreeMap()
Jenkins.instance.pluginManager.plugins.each{
  plugins.put(it.getShortName(),it.getVersionNumber())
}

plugins.each{
 println "${it.getKey()} \t\t ${it.getValue()}"
}

return null