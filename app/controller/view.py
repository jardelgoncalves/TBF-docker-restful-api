from app import app
from flask import jsonify, request, url_for, make_response
import os


@app.route("/ifaces", methods=["GET"])
def get_ifaces():
    """Returns all containers with their respective IP and interfaces (veth)"""

    file =  os.popen("bash %s/app/static/scripts/interface.sh" %os.getcwd().replace(" ","\ "), "r")
    c = file.readlines()
    ifaces = {}

    for iface in c:
        vet_iface = iface.split(":")
        ifaces[vet_iface[0]] = [{"IP":vet_iface[1],"veth":vet_iface[2].replace("\n","")}]

    return jsonify(ifaces)


@app.route("/stats", methods=["GET"])
def stats_host():
    """Returns the RX and TX data of the Docker interface."""
    if request.method == "GET":
        data = request.get_json(force=True)
        file =  os.popen("bash %s/app/static/scripts/stats.sh %s" %(os.getcwd().replace(" ","\ "), data['iface']), "r")
        c = file.readlines()
        try:
            rx=0
            tx=0
            for line in c:
                d = line.split(":")
                rx = d[0]
                tx = d[1].replace('\n','')
            return jsonify({"RX":rx, "TX":tx})
        except IndexError:
            return make_response(jsonify({"error":"Interface does not exist."}),404)


@app.route("/qos/rules", methods=["GET", "DELETE", "POST"])
def qos_rules():
    """Add, List, or Remove QoS rule from the interface of a given container."""

    if request.method == "GET":
        file =  os.popen("bash %s/app/static/scripts/tbf_ifaces.sh" %os.getcwd().replace(" ","\ "), "r")
        c = file.readlines()
        rules = {}
        for line in c:
            vetor = line.split("=")
            ip = vetor[0]
            veth = vetor[1]
            id = vetor[3].replace("\n","")

            rule = vetor[2].split(":")[1].split(" ")
            rate = rule[5]
            burst = rule[7]
            peak = rule[9]
            minburst = rule[11]
            lat = rule[13]

            rules[veth] = {"IP":ip, "ID":id, "rule":{"rate":rate, "burst":burst,
                            "peak":peak, "minburst":minburst,"latency":lat} }
        return jsonify(rules)
    
    elif request.method == "DELETE":
        data = request.get_json(force=True)

        file =  os.popen("bash %s/app/static/scripts/delete_rule.sh %s %s %s" %(os.getcwd().replace(" ","\ "), 
                                                          data['veth'], data['user'], data['pass']), "r")
        c = file.readlines()
        for line in c:
            print c
            if line.replace('\n','') == "0":
                return make_response(jsonify({"result":"success"}),200)
            else:
                return make_response(jsonify({"error":"interface does not exist."}),404)

        return make_response(jsonify({"error":"Rule not applied."}),404)
    
    elif request.method == "POST":
        data = request.get_json(force=True)
        file =  os.popen("bash %s/app/static/scripts/add_rule.sh %s %s %s %s %s %s %s %s" %(os.getcwd().replace(" ","\ "), 
                                            data['user'],data['pass'], data['veth'], data['rate'],
                                            data['burst'], data['latency'], data['peak'], data['minburst']), "r")
        c = file.readlines()

        for line in c:
            if line.replace('\n','') == "0":
                return make_response(jsonify({"result":"success"}),200)
            elif line.replace('\n','') == "1":
                return make_response(jsonify({"error":"interface does not exist."}),404)
        
        return make_response(jsonify({"error":"Rule not applied."}),404)