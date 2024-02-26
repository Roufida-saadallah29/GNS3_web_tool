from pprint import pprint
from unittest import result
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.template import loader
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth.decorators import login_required
from gns3fy import Gns3Connector, Project, Node
# from .forms import ProjectForm
import json
import requests
from netmiko import ConnectHandler
from telnetlib import Telnet
import time

def CreateDevice(request, project_id,template_id ):
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
        messages.error(request, f"{url} : GNS3 server is down.")
        return redirect("/connections")
    server = Gns3Connector(url)
    project = Project(project_id=project_id, connector=server)
    project.get()
    try:  
        node = Node(template_id=template_id, project_id=project_id, connector=server)
        node.create()
        messages.success(request, "Element updated with success")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e: 
        # found = reverse('project-main-dashboard', kwargs={'connection_id': connection_id, 'project_id': project_id})
        return redirect(request.META.get('HTTP_REFERER'))  





def deviceStart(request, project_id, device_id):    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/error")
    server = Gns3Connector(url)
    # project = Project(project_id=project_id, connector=server)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    device.start()
    messages.success(request, f"Device: {device.name} has been started")
    return redirect(request.META.get('HTTP_REFERER'))


def deviceReload(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    device.reload()
    messages.success(request, f"Device: {device.name} has been reloaded")
    return redirect(request.META.get('HTTP_REFERER'))


def deviceSuspend(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    device.suspend()
    messages.success(request, f"Device: {device.name} has been suspended")
    return redirect(request.META.get('HTTP_REFERER'))


def deviceStop(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    device.stop()
    messages.success(request, f"Device: {device.name} has been stopped")
    return redirect(request.META.get('HTTP_REFERER'))



def deviceDelete(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
        messages.error(request, f"{url} : GNS3 server is down.")
        return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    try:
        device.delete()
        messages.success(request, "Element deleted with success")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect(request.META.get('HTTP_REFERER'))


def deviceIndex(request, project_id, device_id):
    template = loader.get_template('device-index.html')
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
        messages.error(request, f"{url} : GNS3 server is down.")
        return redirect("/connections")
    server = Gns3Connector(url)
    project = Project(project_id=project_id, connector=server)
    project.get()
    project.open()
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    templates = {}
    nodes = project.nodes
    for node in nodes:
        if node.console_type == 'none':
            node.update(console_type="telnet", console_auto_start=True)
            node.reload()
        templates[node.template_id] = server.get_template(template_id=node.template_id)["category"].capitalize()
    context = {
        'project' : project,
        'device' : device,
        'templates_dict' : templates,
        'device_id' : device_id,
        'project_id' : project_id,
    }
    return HttpResponse(template.render(context, request))



def deviceRunningConfig(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),

    }
    running_config = None
    try:
        tn = Telnet(host=str(device.console_host), port=device.console)
        prepareTelnet(tn, "connect")
        with ConnectHandler(**cisco1) as net_connect:
            running_config = net_connect.send_command("show running-config")
        net_connect.disconnect()
    except Exception as e:
        running_config = e
    
    return HttpResponse(str(running_config), content_type="application/json")


def deviceIpRoute(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),

    }
    running_config = None
    try:
        tn = Telnet(host=str(device.console_host), port=device.console)
        prepareTelnet(tn, "connect")
        with ConnectHandler(**cisco1) as net_connect:
            running_config = net_connect.send_command("show ip route")
        net_connect.disconnect()
    except Exception as e:
        running_config = e
    
    return HttpResponse(str(running_config), content_type="application/json")


def deviceStartupConfig(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),
    }
    startup_config = ""
    try:
        tn = Telnet(host=str(device.console_host), port=device.console)
        prepareTelnet(tn, "connect")
        with ConnectHandler(**cisco1) as net_connect:
            startup_config = net_connect.send_command("show startup-config")
        net_connect.disconnect()
    except Exception as e:
        startup_config = e
    # tn = Telnet(str(device.console_host), device.console)
    # tn.read_until(b"#").decode("utf-8")
    # tn.write(b'\x15')
    # tn.read_until(b"#").decode("utf-8")
    # tn.write(b'show startup-config\r')
    # c = False
    # for i in range(2):
    #     x = tn.read_until(b"\r").decode("utf-8")
    #     print(x)
    #     if(i != 0):
    #         startup_config+=f"{x}"
    #     time.sleep(0.5)
    # tn.close()
    return HttpResponse(str(startup_config), content_type="application/json")


def deviceGetVlans(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),

    }
    vlans = ""
    try:
        tn = Telnet(host=str(device.console_host), port=device.console)
        prepareTelnet(tn, "connect")
        with ConnectHandler(**cisco1) as net_connect:
            vlans = net_connect.send_command("\r\rshow vlan-switch")
            # print(vlans)
        net_connect.disconnect()
    except Exception as e:
        vlans = e
    return HttpResponse(str(vlans), content_type="application/json")



def devicePingIpAddress(request, project_id, device_id, ip_address):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),

    }
    project = Project(project_id=project_id, connector=server)
    project.get()
    project.open()
    templates = {}
    nodes = project.nodes
    for node in nodes:
        templates[node.template_id] = server.get_template(template_id=node.template_id)["category"].capitalize()
    pingResult = ""
    try:
        tn = Telnet(host=str(device.console_host), port=device.console)
        if templates[device.template_id] == "Guest":
            pingResult = guestPing(tn, ip_address)
        else:
            prepareTelnet(tn, "connect")
            with ConnectHandler(**cisco1) as net_connect:
                pingResult = net_connect.send_command(f"\r\rping {ip_address}")
                print(pingResult)
            net_connect.disconnect()
    except Exception as e:
        pingResult = e
    return HttpResponse(str(pingResult), content_type="application/json")


def deviceCopyRunningToStartup(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    all_result = []
    if device.status != "started":
        return HttpResponse(str("Device is not running!"), content_type="application/json")
    tn = Telnet(str(device.console_host), device.console)
    prepareTelnet(tn, "connect")
    tn.write(b'\x15copy running-config startup-config\r\r')
    c = False
    for i in range(10):
        x = tn.read_until(b"#").decode("utf-8")
        # print(x.split("\n")[-2])
        if "[OK]" in x.split("\n")[-2]:
            c = True
            break
        else:
            time.sleep(1)
    tn.close()
    if c:
        return HttpResponse(str("Config copied successfully!"), content_type="application/json")
    else:
        return HttpResponse(str("Config copied successfully!"), content_type="application/json")


def deviceCreateVlan(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    if device.status != "started":
        return HttpResponse(str("Device is not running!"), content_type="application/json")
    else:
        if request.method == "POST":
            form = CreateVlanForm(request.POST)  
            if form.is_valid():  
                vlan_number = request.POST['vlanNumber']
                cisco1 = {
                    "device_type": "cisco_ios_telnet",
                    "host": str(device.console_host),
                    "port": str(device.console),
                    # "fast_cli": False,  # Notice the item here
                }
                result = ""
                tn = Telnet(host=str(device.console_host), port=device.console)
                prepareTelnet(tn, "connect")
                net_connect =  ConnectHandler(**cisco1)
                # net_connect.enable()
                cmd = '\rvlan database \rvlan '+str(vlan_number)+'\rexit\r'
                result += net_connect.send_command_timing(cmd)
                # result += "\n" 
                # result += f"{net_connect.send_config_set(commands)}\n"
                net_connect.disconnect()
                # print(result)
                return HttpResponse(str(result), content_type="application/json")
        else:
            # raise Exception(device)
            template = loader.get_template('new_vlan.html')
            project = Project(project_id=project_id, connector=server)
            project.get()
            project.open()
            context = {
                'project' : project,
                'device' : device,
                'project_id' : project_id,
        'device_id' : device_id,
            }
            return HttpResponse(template.render(context, request))


def deviceVlanAccessMode(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),
        # "fast_cli": False,  # Notice the item here
    }
    if device.status != "started":
        return HttpResponse(str("Device is not running!"), content_type="application/json")
    else:
        if request.method == "POST":
            interfaces = request.POST.getlist('interfaces[]')
            # vlan_mask = request.POST['vlanMask']
            # vlan_default_gateway = request.POST['vlanDefaultGateway']
            
            list = [x.split("+") for x in interfaces]
            result = ""
            tn = Telnet(host=str(device.console_host), port=device.console)
            prepareTelnet(tn, "connect")
            net_connect =  ConnectHandler(**cisco1)
            for part in list:
                if part[1] == "add":
                    commands = [
                        f"interface {part[0]}",
                        f"switchport mode {part[2]}",
                        f"\r" if part[2] == "trunk" else f"switchport access vlan {part[3]}",
                        f"no shutdown \r",
                        f"exit"
                    ]
                else:
                    commands = [
                        f"interface {part[0]}",
                        f"\r" if part[2] == "trunk" else f"no switchport access vlan {part[3]}\r",
                        f"no switchport mode \r",
                        f"no shutdown \r",
                        f"exit"
                    ]
                result += f"{net_connect.send_config_set(commands)}\n"
            prepareTelnet(tn, "disconnect")
            net_connect.disconnect()
            # # print(result)
            return HttpResponse(str(result), content_type="application/json")
        else:
            template = loader.get_template('vlan_access_mode.html')
            project = Project(project_id=project_id, connector=server)
            project.get()
            project.open()
            tn = Telnet(host=str(device.console_host), port=device.console)
            prepareTelnet(tn, "connect")
            net_connect =  ConnectHandler(**cisco1)
            vlans = getVlansFromOutput(net_connect.send_command('show vlan-switch brief'))
            prepareTelnet(tn, "disconnect")
            net_connect.disconnect()
            context = {
                'project' : project,
                'device' : device,
                'vlans' : vlans,
                'project_id' : project_id,
                'device_id' : device_id,
            }
            return HttpResponse(template.render(context, request))
            
def deviceAddStaticRoute(request, project_id, device_id):
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),
        # "fast_cli": False,  # Notice the item here
    }
    if device.status != "started":
        return HttpResponse(str("Device is not running!"), content_type="application/json")
    else:
        if request.method == "POST":
            form = AddStaticRouteForm(request.POST)  
            if form.is_valid():  
                result = ""
                route_ip_address = request.POST['routeIpAddress']
                route_action = request.POST['routeAction']
                route_mask = request.POST['routeMask']
                route_default_gateway = request.POST['routeDefaultGateway']
                tn = Telnet(host=str(device.console_host), port=device.console)
                prepareTelnet(tn, "connect")
                net_connect =  ConnectHandler(**cisco1)
                if route_action == "add":
                    cmd = '\r\nconf t \r\nip route ' + str(route_ip_address) + " " + str(route_mask) + " " + str(route_default_gateway) + " \r\n end \r"
                else:
                    cmd = '\r\nconf t \r\nno ip route ' + str(route_ip_address) + " " + str(route_mask) + " " + str(route_default_gateway) + " \r\n end \r"
                result = net_connect.send_command_timing(cmd)
                prepareTelnet(tn, "disconnect")
                net_connect.disconnect()
                
                return HttpResponse(str(result), content_type="application/json")
            else:
                print(form.errors)
                return HttpResponse(str("Error"), content_type="application/json")
        else:
            # raise Exception(device)
            template = loader.get_template('add_static_route.html')
            project = Project(project_id=project_id, connector=server)
            project.get()
            project.open()
            context = {
                'project' : project,
                'device' : device,
                'project_id' : project_id,
                'device_id' : device_id,
            }
            return HttpResponse(template.render(context, request))

def deviceInterfacesIpAddress(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    cisco1 = {
        "device_type": "cisco_ios_telnet",
        "host": str(device.console_host),
        "port": str(device.console),
    }
    if device.status != "started":
        return HttpResponse(str("Device is not running!"), content_type="application/json")
    else:
        if request.method == "POST":
            interfaces = request.POST.getlist('interfaces[]')
            list = [x.split("+") for x in interfaces]
            result = ""
            tn = Telnet(host=str(device.console_host), port=device.console)
            prepareTelnet(tn, "connect")
            net_connect =  ConnectHandler(**cisco1)
            for part in list:
                commands = [
                    f"configure terminal\r",
                    f"interface {part[0]}\r",
                    f"ip address {part[1]} {part[2]}\r",
                    f"no shutdown\r"
                    f"exit\r"
                    f"end\r"
                ]
                for cmd in commands:
                    result += f"{net_connect.send_command_timing(cmd)}\n"
            prepareTelnet(tn, "disconnect")
            net_connect.disconnect()
            return HttpResponse(str(result), content_type="application/json")
        else:
            template = loader.get_template('interfaces_ip_address.html')
            project = Project(project_id=project_id, connector=server)
            project.get()
            project.open()
            context = {
                'project' : project,
                'device' : device,
                'project_id' : project_id,
                'device_id' : device_id,
            }
            return HttpResponse(template.render(context, request))


def deviceGuestIpAddress(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    if device.status != "started":
        return HttpResponse(str("Device is not running!"), content_type="application/json")
    else:
        if request.method == "POST":
            form = GuestIpAddressForm(request.POST)  
            if form.is_valid():  
                guest_ip_address = request.POST['guestIpAddress']
                guest_mask = request.POST['guestMask']
                guest_default_gateway = request.POST['guestDefaultGateway']
                tn = Telnet(host=str(device.console_host), port=device.console)
                sendGuestIpAddress(tn, guest_ip_address, guest_mask, guest_default_gateway)
                return HttpResponse(str("Done"), content_type="application/json")
            else:
                return HttpResponse(str("Error"), content_type="application/json")
        else:
            # raise Exception(device)
            template = loader.get_template('guest_ip_address.html')
            project = Project(project_id=project_id, connector=server)
            project.get()
            project.open()
            context = {
                'project' : project,
                'device' : device,
                'project_id' : project_id,
                'device_id' : device_id,
            }
            return HttpResponse(template.render(context, request))


def deviceGuestShowIp(request, project_id, device_id):
    
    url = f"http://localhost:3080"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
            messages.error(request, f"{url} : GNS3 server is down.")
            return redirect("/connections")
    server = Gns3Connector(url)
    device = Node(project_id=project_id, node_id=device_id, connector=server)
    device.get()
    result = ""
    try:
        tn = Telnet(host=str(device.console_host), port=device.console)
        result = guestShowIp(tn)
    except Exception as e:
        result = e
    return HttpResponse(str(result), content_type="application/json")
