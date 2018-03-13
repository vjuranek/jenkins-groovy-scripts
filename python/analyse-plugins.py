#!/usr/bin/env python3

import os
import xml.etree.ElementTree as etree

JENKINS_HOME = os.environ['JENKINS_HOME'] if 'JENKINS_HOME' in os.environ else '/var/lib/jenkins'
JOBS_DIR = JENKINS_HOME + "/jobs"
PLUGINS_DIR = JENKINS_HOME + "/plugins"


def plugins_from_config(config_path):
    plugins = set()
    xml = etree.parse(config_path)
    plugin_elems = xml.findall('.//*[@plugin]')
    for el in plugin_elems:
        val = el.attrib['plugin']
        if '@' not in val:
            continue
        else:
            plugins.add(val.split('@')[0])
    return plugins


def _parse_manifest(content, skip_optional):
    plugins = set()
    try:
        start = content.index("Plugin-Dependencies:") + len("Plugin-Dependencies:")
    except ValueError:
        return plugins
    try:
        end = content.index("Plugin-Developers")
    except ValueError:
        end = len(content)
    deps = content[start:end]
    deps = deps.replace('\n ', '')  # new line + one space indentation
    deps = deps.replace('\r', '')  # some plugins contains windows line breaks
    ps = deps.strip().split(',')
    for p in ps:
        parts = p.split(':')
        try:
            optional = False
            if len(parts) > 2 and parts[2].index("=optional") == 0:
                optional = True
        except ValueError:
            pass
        if optional and skip_optional:
            continue
        else:
            plugins.add(parts[0])
    return plugins


def plugins_from_manifest(manifest_path, skip_optional=True):
    plugins = set()
    with open(manifest_path, 'r') as mf:
        content = mf.read()
        plugins = _parse_manifest(content, skip_optional)
    return plugins


def plugin_deps(plugin_name):
    plugins = set()
    plugin_dir = os.path.join(PLUGINS_DIR, plugin_name)
    if os.path.isdir(plugin_dir):
        manifest = os.path.join(PLUGINS_DIR, plugin_name, "META-INF/MANIFEST.MF")
        if os.path.isfile(manifest):
            dep_plugins = plugins_from_manifest(manifest)
            plugins = plugins.union(dep_plugins)
            # search also dependencies of dependent plugins
            for plugin in dep_plugins:
                plugins = plugins.union(plugin_deps(plugin))
    return plugins


def get_job_configs(jobs_dir):
    configs = set()
    for job in os.listdir(jobs_dir):
        job_dir = os.path.join(jobs_dir, job)
        if os.path.isdir(job_dir):
            cfg = os.path.join(job_dir, "config.xml")
            if os.path.isfile(cfg):
                configs.add(cfg)
    return configs


def get_global_configs(jenkins_home):
    configs = set()
    for file in os.listdir(jenkins_home):
        cfg = os.path.join(jenkins_home, file)
        if os.path.isfile(cfg) and file.endswith(".xml"):
            configs.add(cfg)
    return configs


def job_plugins():
    plugins = set()
    for conf in get_job_configs(JOBS_DIR):
        plugins = plugins.union(plugins_from_config(conf))
    return plugins


def global_config_plugins():
    plugins = set()
    for conf in get_global_configs(JENKINS_HOME):
        plugins = plugins.union(plugins_from_config(conf))
    return plugins


def plugin_dependencies(plugs):
    plugins = set()
    for plugin in plugs:
        plugins = plugins.union(plugin_deps(plugin))
    return plugins


def main():
    jp = job_plugins()
    print(jp)
    gp = global_config_plugins()
    print(gp)
    dp = plugin_dependencies(jp.union(gp))
    print(dp)
    plugins = sorted(jp.union(gp).union(dp))
    for plugin in plugins:
        print(plugin)
    print("size: " + str(len(plugins)))

if __name__ == "__main__":
    main()
