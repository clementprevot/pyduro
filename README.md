[![GitHub Latest Release][releases_shield]][latest_release]
[![GitHub All Releases][downloads_total_shield]][releases]
[![Buy me a coffee][buy_me_a_coffee_shield]][buy_me_a_coffee]
[![PayPal.Me][paypal_me_shield]][paypal_me]

[latest_release]: https://github.com/clementprevot/pyduro/releases/latest
[releases_shield]: https://img.shields.io/github/release/clementprevot/pyduro.svg?style=for-the-badge
[releases]: https://github.com/clementprevot/pyduro/releases
[downloads_total_shield]: https://img.shields.io/github/downloads/clementprevot/pyduro/total?style=for-the-badge
[buy_me_a_coffee_shield]: https://img.shields.io/static/v1.svg?label=%20&message=Buy%20me%20a%20pizza&color=ff6937&style=for-the-badge&logo=buy%20me%20a%20coffee&logoColor=white
[buy_me_a_coffee]: https://www.buymeacoffee.com/clementprevot
[paypal_me_shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&style=for-the-badge&logo=paypal
[paypal_me]: https://paypal.me/clementprevot

# PyDuro

A Pypi library to communicate with Aduro (H1) wood/pellet burner via NBE
communication.

## About

This library is intented to communicate with NBE capable burners (typically
Adura hybrid stoves).

### Request

NBE is an UDP protocol that uses ASCII frames to communicate. Here is an example
frame (this one is used to discover a burner):

```
abcdefghijkl041837 \x02000012345678904361465775pad 013NBE Discovery\x04
```

And here the different part of the frame:

* **abcdefghijkl** - `appId`, 12 alphanumerical (upper and lowercase) characters -
  Uniquely identify the application that is talking with the oven _(you can
  put here whatever you want)_
* **123456** - `controllerId`, 6 digits - This is the "Serial number" of your
  oven _(the same as the one you entered in the official Aduro application, you
  can find it on a sticker on the oven, often inside of the door)_
* **space** or **\*** or **-** - Encryption level of the frame _(' ' = not
  encrypted, '*' = RSA encrypted, '-' = XTEA encrypted)_
* **\x02** - `startChar`, the ASCII character `0x02` _(so 1 char, not "\x02")_ -
  This is the separator to identify the beginning of the request
* **00** - `function`, 2 digits - Identify the type of request _(see below)_
* **00** - `sequenceNumber`, 2 digits - To identify the request when run in
  sequence _(optional, you can leave this at 00 if you don't care about the
  order of your requests)_
* **1234567890** - `pinCode`, 10 digit - The password to connect to your oven
  _(the same as the one you entered in the official Aduro application, you can
  find it on a sticker on the oven, often inside of the door)_
* **4361465775** - `time`, 10 digits - The timestamp at which the request as
  been issued _(`'{:0>10.10}'.format(str(time()))` in Python do the trick)_
* **pad** _(literally the string "pad ") - Extra space reserved for future use
* **013** - `payloadSize`, 3 digits - The size of the actual payload of the
  request _(that comes right after this)_
* **NBE Discovery** - `payload`, max 495 bytes - The actual payload of the
  request _(here in the example it's a discovery request)_.
* **\x04** - `endChar`, the ASCII character `0x04` _(so 1 char, not "\x04")_ -
  This is the separator to identify the end of the payload

### Response

A response will always be formed in pretty much the same way:

```
abcdefghijkl123456\x0200000065Serial=123456;IP=192.168.1.250;Type=v13std;Ver=705;Build=38;Lang=0\x04
```

* **abcdefghijkl** - `appId`, 12 alphanumerical (upper and lowercase) characters -
  Uniquely identify the application that the oven  is talking to
* **123456** - `controllerId`, 6 digits - This is the "Serial number" of the
  oven responding
* **\x02** - `startChar`, the ASCII character `0x02` _(so 1 char, not "\x02")_ -
  This is the separator to identify the beginning of the response
* **00** - `function`, 2 digits - Identify the type of response _(see below)_
* **00** - `sequenceNumber`, 2 digits - To identify the request this response is
  for when using a sequence
* **0** - `status`, 1 digit - The status of the response _(0 = success, >0 =
  error)_
* **013** - `payloadSize`, 3 digits - The size of the actual payload of the
  response _(that comes right after this)_
* **Serial=12345;IP=192.168.1.250;Type=v13std;Ver=705;Build=38;Lang=0** -
  `payload`, max 1007 bytes - The actual payload of the response _(here in the
  example it's a discovery response in the form of a semicolon separated list of
  key/values pair)_.
* **\x04** - `endChar`, the ASCII character `0x04` _(so 1 char, not "\x04")_ -
  This is the separator to identify the end of the payload

### Functions

There is a limited set of functions you can use in the NBE protocol:

* **0**: Discovery
* **1**: Read settings value
* **2**: Set settings value
* **3**: Read setup range
* **4**: Read operating data
* **5**: Read advanced data
* **6**: Read consumption data
* **7**: Read chart data
* **8**: Read event log
* **9**: Read info
* **10**: Read available programs

> Note that your burner might not support all of them and might also support
> others (for example, `11` is a supported type on Aduro H1 burners).

### More info

You can learn more about NBE with
[this repository](https://github.com/motoz/nbetest)
_(I highly recommend you to play with the CLI to discover more about the protocol)_
and in particular
[this documentation](https://github.com/motoz/nbetest/blob/master/protocol.md)
as well as the various implementations.

You can also read [this issue](https://github.com/clementprevot/pyduro/issues/1)
and the implementation of the protocol in the PyDuro library.

## Installation

```bash
pip install pyduro
```

## Lib usage

Simply import the actions and use them:

```python
from pyduro.actions import discover, get, set, raw

discover.run()
get.run(
  burner_address="<burner IP address>",
  serial="<burner serial number>",
  pin_code="<burner pin code>",
  function_name="<settings|range|operating|advanced|consumption|chart|logs|info|versions>",
  path="<path>"
)
set.run(
  burner_address="<burner IP address>",
  serial="<burner serial number>",
  pin_code="<burner pin code>",
  path="<path>"
  value="<value>"
)
raw.run(
  burner_address="<burner IP address>",
  serial="<burner serial number>",
  pin_code="<burner pin code>",
  function_id="<function ID>",
  payload="<payload>"
)
```

### Response

Every response from a burner will be composed with the same fields:

* `frame`: the whole raw NBE frame received
* `burner_address`: the burner IP address from which the response originated
* `burner_port`: the burner UDP port from which the response originated
* `app_id`: the application ID the response is intended to
  _(when using PyDuro will always be `___pyduro___`)_
* `serial`: the burner serial number from which the response originated
* `function`: the function identifier the response is intended to
* `sequence_number`: the identifier of the request the response is intended to
* `status`: the status of the response _(0 = success, >0 = error)_
* `payload_size`: the size of the payload of the response
* `payload`: the actual response payload

You can also use the `parse_payload` method that will return:

* a string if the payload is a string
* a dict if the payload is a semicolon separated list of fields _(`name=value`)_
* a list of the payload is a semicolon separated list of values

## CLI usage

### Integrated help

```bash
python -m pyduro --help
```

### Discover a burner

```bash
python -m pyduro [discover]
```

The CLI will exit with 0 if a burner is found, 1 otherwise.

### Get the status of a burner

```bash
python -m pyduro -b <burner IP address> -s <burner serial number> -p <burner pin code> status
```

The result will be output as a JSON object that you can then manipulate with
`jq` for example.

The CLI will exit with the return code return by the burner (0 = success, >0 =
error).

**Examples**

```bash
python -m pyduro -b 192.168.1.250 -s 1234 -p 12345678 status

> {
>   "boiler_temp": "14.9",
>   "boiler_ref": "20.0",
>   "content": "-2038",
>   "dhw_temp": "13.6",
>   "dhw_ref": "0.0",
>   [...]
> }
```

### Get information from a burner

```bash
python -m pyduro -b <burner IP address> -s <burner serial number> -p <burner pin code> get <settings|range|operating|advanced|consumption|chart|logs|info|versions> "<path>"
```

The result will be output as a JSON object that you can then manipulate with
`jq` for example.

The CLI will exit with the return code return by the burner (0 = success, >0 =
error).

> For `logs` action, you can pass "now" as path (which is also the default
> value) to get the latest logs from your burner.

> For `settings` action, you have to pass one of the valid following path:
>
> * "boiler",
> * "hot_water"
> * "regulation"
> * "weather"
> * "weather2"
> * "oxygen"
> * "cleaning"
> * "hopper"
> * "fan"
> * "auger"
> * "ignition"
> * "pump"
> * "sun"
> * "vacuum"
> * "misc"
> * "alarm"
> * "manual"
>
> To see all sub element of a path, add `.*` at the end of the path.  
> To see a specific element of a path, add `.<element name>` at the end of the
> path.

> For `consumption` action, you can pass one of the following path:
>
> * "total_hours",
> * "total_days"
> * "total_months"
> * "total_years"
> * "dhw_hours"
> * "dhw_days"
> * "dhw_months"
> * "dhw_years"
> * "counter"

**Examples**

```bash
python -m pyduro -b 192.168.1.250 -s 1234 -p 12345678 get operating

> {
>   "NA": "38",
>   "air_flow": "0",
>   "air_quality": "0",
>   "ashbox_contact": "0.0",
>   "ashbox_minutes": "0.0",
>   "back_pressure": "0",
>   "boiler_pump_state": "0",
>   "boiler_ref": "19.0",
>   [...]
> }
```

```bash
python -m pyduro -b 192.168.1.250 -s 1234 -p 12345678 get operating "boiler_ref"

> "boiler_ref=19.0"
```

```bash
python -m pyduro -b 192.168.1.250 -s 1234 -p 12345678 get settings "misc.*"

> {
>   [...]
>   "start": "0",
>   "stop": "0",
>   [...]
> }
```

```bash
python -m pyduro -b 192.168.1.250 -s 1234 -p 12345678 get settings "misc.start"

> "start=0"
```

> Note that you can pass "*" as a path to get the full response from your
> burner.  
> If you don't give a pass (or give an empty one) then "*" will be used
> as default.

### Update a burner's setting

```bash
python -m pyduro -b <burner IP address> -s <burner serial number> -p <burner pin code> set "<path>" "<value>"
```

The CLI will exit with the return code return by the burner (0 = success, >0 =
error).

**Examples**

```bash
python -m pyduro -b 192.168.1.250 -s 1234 -p 12345678 set "misc.start" "1"
```

```bash
python -m pyduro -b 192.168.1.250 -s 1234 -p 12345678 set "misc.stop" "1"
```
