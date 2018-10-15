# QoSDocker RESTFul API
Simple RESTFul API for obtaining information from the Docker interface and for enforcing TBF-based QoS policies.


## Show Interfaces
Returns all containers with their respective IP and interfaces (veth)

#### URL
- `/ifaces`

#### Method:
`GET`
#### Success Response:
- <b>Code</b>: 200
- <b>Content:</b> `{"e943f949c929": [{"IP": "172.17.0.2", "veth": "veth0167b74"}]}}` 

OR

- <b>Code</b>: 200
- <b>Content</b>: `{}`

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
`{"iface":"target interface"}`

#### Success Response:
- <b>Code:</b> 200
- <b>Content:</b> `{"veth0167b74": {"ID": "e943f949c929", "IP": "172.17.0.2", "rule": {"burst": "4Kb", "latency": "49.9ms", "minburst": "1519b", "peak": "91Kbit", "rate": "90Kbit"}}}` or `{}`

#### Error Response:
- <b>Code:</b> 404
- <b>Content:</b> `{"error":"Interface does not exist."}`

- `/qos/rules` - Add, List, or Remove QoS rule from the interface of a given container.
`
