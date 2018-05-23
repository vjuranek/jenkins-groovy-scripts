view = Jenkins.instance.getView("to-remove")
view.items.each{
  println "Deleting ${it.displayName}"
  it.delete()
}
return true
