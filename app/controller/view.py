from app import app
from flask import jsonify, request, url_for, request
import os


@app.route("/ifaces", methods=["GET"])
def get_ifaces():
    file =  os.popen("bash %s/app/static/scripts/interface.sh" %os.getcwd().replace(" ","\ "), "r")
    c = file.readlines()
    ifaces = {}

    for iface in c:
        vet_iface = iface.split(":")
        ifaces[vet_iface[0]] = [{"IP":vet_iface[1],"veth":vet_iface[2].replace("\n","")}]


    return jsonify(ifaces)


@app.route("/stats/<string:interface>", methods=["GET"])
def stats_host(interface):

    file = os.popen("ifconfig %s | tail -n2 | head -n 1 | tr -s ' '" %(interface), "r")
    c = file.readlines()
    line = c[0].split(" ")

    rx = float(line[2].split(":")[1])
    tx = float(line[6].split(":")[1])
        
    return jsonify({"rx":rx, "tx":tx})




@app.route("/qos/add/tbf", methods=["GET", "POST"])
def qos_add_tbf():
    latency     = request.json["latency"]
    burst       = request.json["burst"]
    rate        = request.json["rate"]
    peakrate    = request.json["peakrate"]
    minburst    = request.json["minburst"]