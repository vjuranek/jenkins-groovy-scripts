import org.jenkinsci.plugins.postbuildscript.PostBuildScript

Jenkins.instance.getAllItems(AbstractProject.class).each{job ->
    job.publishersList.each{
      if (it instanceof PostBuildScript) {
        println job.displayName
      }
    }
}

return null