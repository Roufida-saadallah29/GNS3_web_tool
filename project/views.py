from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from gns3fy import Gns3Connector, Project
from django.template import loader
import requests
import subprocess
import json
from django.contrib import messages


def start_gns3():
    try:
        subprocess.Popen(['gns3'])
    except Exception as e:
        print("Error starting GNS3:", e)
def index(request):
    template = loader.get_template('project.html')
    return HttpResponse(template.render(request))

def home(request):
    template = loader.get_template('project.html')
    url = "http://localhost:3080"
    # Start GNS3 if not already running
    # start_gns3()
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except Exception as e:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/error") 
    server = Gns3Connector(url)
    projects_list = server.get_projects()
    project_name = "gns3tool"
    project_info = None
    
    for project in projects_list:
        if project["name"] == project_name:
            project_info = project
            break

    if not project_info:
        project_info = server.create_project(name=project_name)

    project = Project(project_id=project_info["project_id"], connector=server)
    project.get()
    project.open()
    nodes = project.nodes
    links = project.links
    stats = {
        "started" : 0,
        "suspended" : 0,
        "stopped" : 0
    }
    templates_list = server.get_templates()
    # Organize data by category
    categories = {}
    for item in templates_list:
        category = item['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    templates = {}
    for node in nodes:
        # raise Exception(node.template)
        if node.console_type == 'none':
            node.update(console_type="telnet", console_auto_start=True)
            node.reload()
        if node.status is not None:
            stats[node.status] += 1
        templates[node.template_id] = server.get_template(template_id=node.template_id)["category"].capitalize()
    # nodes_list = [any_to_json(x.__dict__) for x in nodes]
    # links_list = [any_to_json(x.__dict__) for x in links]
    context = {
        'project' : project,
        'nodes_list' : nodes,
        'templates_dict' : templates,
        'templates_list' : templates_list,
        'categories' :categories,
        # 'links_list': links_list, 
        'stats' : stats,
        'project_id' : project_info["project_id"],
    }
    return HttpResponse(template.render(context, request))


def projectMainDashboard(request, project_id):
    template = loader.get_template('project.html')
    url = "http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except Exception as e:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/error")
    server = Gns3Connector(url)
    project = Project(project_id=project_id, connector=server)
    project.get()
    project.open()
    nodes = project.nodes
    links = project.links
    stats = {
        "started" : 0,
        "suspended" : 0,
        "stopped" : 0
    }
    templates = {}
    for node in nodes:
        # raise Exception(node.template)
        if node.console_type == 'none':
            node.update(console_type="telnet", console_auto_start=True)
            node.reload()
        stats[node.status] += 1
        templates[node.template_id] = server.get_template(template_id=node.template_id)["category"].capitalize()
    # nodes_list = [any_to_json(x.__dict__) for x in nodes]
    # links_list = [any_to_json(x.__dict__) for x in links]
    context = {
        'project' : project,
        'nodes_list' : nodes,
        'templates_dict' : templates,
        # 'links_list': links_list, 
        'stats' : stats,
        'project_id' : project_id,
    }
    return HttpResponse(template.render(context, request))

def projectMainNetwork(request, project_id):
    template = loader.get_template('project.html')
    url = "http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except Exception as e:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/error")
    server = Gns3Connector(url)
    project = Project(project_id=project_id, connector=server)
    project.get()
    nodes = project.nodes
    links = project.links
    stats = {
        "nodes" : [{
            "node_id" : n.node_id, 
            "name" : n.name, 
            "node_type" : n.node_type,
            "status" : n.status,
            "console" : n.console,
            "x" : n.x,
            "y" : n.y,
            "console_host" : n.console_host,
            "console_type" : n.console_type,
            "symbol" : f"http://localhost:3080/v2/symbols/{n.symbol}/raw",
        } for n in nodes],
        "links" : [{
            "link" : [l.__dict__[v] for v in l.__dict__],
            "link_id" : l.link_id, 
            "link_type" : l.link_type, 
            "source" : l.nodes[0]["node_id"],
            "source_port" : l.nodes[0]["port_number"],
            "target" : l.nodes[1]["node_id"],
            "target_port" : l.nodes[1]["port_number"],
        } for l in links],
    }
    
    return HttpResponse(json.dumps(stats, default=lambda o: '<not serializable>'), content_type="application/json")
    

