# QoS Docker RESTFul API
Simple RESTFul API for obtaining information from the Docker interface and for enforcing TBF-based QoS policies.

### Pendencies
```
pip install -r requeriments.txt
```

### Running
```
python run.py
```

## Show Interfaces
Returns all containers with their respective IP and interfaces (veth)

#### URL
- `/ifaces`

#### Method:
`GET`
#### Success Response:
- <b>Code</b>: 200
- <b>Content:</b> `{"e943f949c929": [{"IP": "172.17.0.2", "veth": "veth0167b74"}]}` 

OR

- <b>Code</b>: 200
- <b>Content</b>: `{}`

#### Sample Call
- Using `curl`
```
$  curl -X GET http://localhost:5000:/ifaces
{
   "e943f949c929": [
      {
         "IP": "172.17.0.2",
         "veth": "veth0167b74"
      }
   ]
}
```
- Using the library `requests` (python)
```
>> import requests
>> r = requests.get("http://localhost:5000/ifaces")
>> r.text
{
  "e943f949c929": [
     {
        "IP": "172.17.0.2",
        "veth": "veth0167b74"
     }
   ]
}
```

<br><br>
## Get interface statistics
Returns the RX and TX data of the Docker interface.

#### URL
- `/stats`

#### Methods:
`GET`

#### URL Params:
`None`

#### Data Params:
```
{
  "iface":"<target interface>"
}
```

#### Success Response:
- <b>Code:</b> 200
- <b>Content:</b> `{"veth0167b74": {"ID": "e943f949c929", "IP": "172.17.0.2", "rule": {"burst": "4Kb", "latency": "49.9ms", "minburst": "1519b", "peak": "91Kbit", "rate": "90Kbit"}}}` or `{}`

#### Error Response:
- <b>Code:</b> 404
- <b>Content:</b> `{"error":"Interface does not exist."}`

#### Sample Call
- Using `curl`
```
$  curl -X GET -d '{"iface":"docker0"}' http://localhost:5000:/stats
{
   "RX": "0", 
   "TX": "8898"
}
```
- Using the library `requests` (python)
```
>> import requests
>> r = requests.get("http://localhost:5000/stats", data='{"iface":"docker0"}')
>> r.text
{
   "RX": "0", 
   "TX": "8898"
}
```
<br><br>
## Adding, listing, and removing rules
Add, List, or Remove QoS rule from the interface of a given container.

#### URL
- `/qos/rules`

#### Methods:
`GET`,`POST` and `DELETE`

#### URL Params:
`None`

#### Data Params:
- if the method is `DELETE`:
```
{
   "veth":"<target interface>",
   "user":"<host user (root privileges required)>", 
   "pass":"<user password>"
 }
```
 
- if the method is `POST`:
```
{
   "veth":"<target interface>",
   "user":"<host user (root privileges required)>", 
   "pass":"<user password>",
   "rate":"<average rate>",
   "burst":"<bucket size>", 
   "latency":"<packet waiting time waiting for tokens>",
   "peak":"<peak gust rate>",
   "minburst":"<number of bytes counted per packet>"
   
 }
```
#### Success Response:
- <b>Method GET</b>
- <b>Code:</b> 200
- <b>Content:</b> `{"veth0167b74": {"ID": "e943f949c929", "IP": "172.17.0.2", "rule": {"burst": "4Kb", "latency": "49.9ms", "minburst": "1519b", "peak": "91Kbit", "rate": "90Kbit"}}}`

<br>

- <b>Method POST or DELETE</b>
- <b>Code:</b> 200
- <b>Content:</b> `'{"result":"success"}'`

#### Error Response:
- <b>Code:</b> 404
- <b>Content:</b> `{"error":"Interface does not exist."}`

OR

- <b>Code:</b> 404
- <b>Content:</b> `{"error":"Rule not applied."}`


#### Sample Call

#### GET
- Using `curl`

```
$  curl -X GET http://localhost:5000:/qos/rules
{
  "veth0167b74": {
    "ID": "e943f949c929", 
    "IP": "172.17.0.2", 
    "rule": {
      "burst": "4Kb", 
      "latency": "49.9ms", 
      "minburst": "1519b", 
      "peak": "91Kbit", 
      "rate": "90Kbit"
    }
  }
}
```

- Using the library `requests` (python)
```
>> import requests
>> r = requests.get("http://localhost:5000/qos/rules")
>> r.text
{
  "veth0167b74": {
    "ID": "e943f949c929", 
    "IP": "172.17.0.2", 
    "rule": {
      "burst": "4Kb", 
      "latency": "49.9ms", 
      "minburst": "1519b", 
      "peak": "91Kbit", 
      "rate": "90Kbit"
    }
  }
}
```

#### DELETE
- Using `curl`
```
$  curl -X DELETE -d '{"veth":"veth0167b74","user":"root", "pass":"123"}' http://localhost:5000:/qos/rules
{
  "result": "success"
}
```
- Using the library `requests` (python)
```
>> import requests
>> r = requests.delete("http://localhost:5000/qos/rules", data='{"veth":"veth0167b74","user":"root", "pass":"123"}')
>> r.text
{
  "result": "success"
}
```

#### POST
- Using `curl`
```
$  curl -X POST -d '{"veth":"veth0167b74","user":"root", "pass":"123","rate":"90kbit", "burst":"32kbit", "latency":"50ms", "peak":"91kbit", "minburst":"1520"}' http://localhost:5000:/qos/rules
{
  "result": "success"
}
```
- Using the library `requests` (python)
```
>> import requests
>> r = requests.post("http://localhost:5000/qos/rules", data='{"veth":"veth0167b74","user":"root", "pass":"123","rate":"90kbit", "burst":"32kbit", "latency":"50ms", "peak":"91kbit", "minburst":"1520"}')
>> r.text
{
  "result": "success"
}
```
