/**
 * Prints all jobs which are not in any view.
 */

import jenkins.model.Jenkins;
import hudson.model.*

public void addAllJobs(View view, Set<String> jobs){
  if(view instanceof ViewGroup) {
    for(View v: view.getViews()) {
      addAllJobs(v, jobs);
    }
    if(view.getItems()!=null) {
      for(Item i: view.getItems()) {
        jobs.add(i.getDisplayName());
      }
    }
  }
  else {
     if(!(view instanceof ProxyView) && !view.name.equals("All")) {
      for(Item i: view.getItems()){
        jobs.add(i.getDisplayName());
      }
     }
  }
}

Set jobsInViews = new HashSet()
Jenkins.instance.views.each {
  addAllJobs(it, jobsInViews)
}

println("=====================")
println("Jobs not in any view:")
Jenkins.instance.items.each {
  if (!jobsInViews.contains(it.displayName))
    println(it.displayName)
}
println("=====================")

return null