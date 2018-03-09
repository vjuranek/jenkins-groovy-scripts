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


def plugins_from_manifest(manifest_path):
    plugins = set()
    with open(manifest_path, 'r') as mf:
        for line in mf.readlines():
            if line.startswith("Plugin-Dependencies:"):
                ps = line.strip("Plugin-Dependencies:").strip().split(',')
                for p in ps:
                    plugins.add(p.split(':')[0])
    return plugins


def plugin_deps(plugin_name):
    plugins = set()
    plugin_dir = os.path.join(PLUGINS_DIR, plugin_name)
    if os.path.isdir(plugin_dir):
        manifest = os.path.join(PLUGINS_DIR, plugin_name, "META-INF/MANIFEST.MF")
        if os.path.isfile(manifest):
            plugins = plugins.union(plugins_from_manifest(manifest))
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


def job_plugins():
    plugins = set()
    for conf in get_job_configs(JOBS_DIR):
        plugins = plugins.union(plugins_from_config(conf))
    return plugins


def plugins_from_deps(plugs):
    plugins = set()
    for plugin in plugs:
        plugins = plugins.union(plugin_deps(plugin))
    return plugins


def main():
    jp = job_plugins()
    print(jp)
    dp = plugins_from_deps(jp)
    print(dp)
    plugins = sorted(jp.union(dp))
    for plugin in plugins:
        print(plugin)
    print("size: " + str(len(plugins)))

if __name__ == "__main__":
    main()
