"""containers provides the operations against containers for a Podman service."""
import json
import logging

import podman.errors as errors


def list_containers(api):
    """List all containers for a Podman service."""
    response = api.request("GET", api.join("/containers/json"))
    return json.loads(response.read())


def inspect(api, name):
    """Report on named container for a Podman service.
       Name may also be a container ID.
    """
    try:
        response = api.request(
            "GET", api.join("/containers/{}/json".format(api.quote(name)))
        )
        return json.loads(response.read())
    except errors.NotFoundError as e:
        _report_not_found(e, e.response)


def kill(api, name, signal=None):
    """kill named/identified container"""
    path = "/containers/{}/kill".format(api.quote(name))
    if signal is not None:
        path = api.join(path, {"signal": signal})
    else:
        path = api.join(path)

    try:
        response = api.request("POST", path)
        response.read() # returns an empty bytes object
        # return json.loads(response.read())
        return True
    except errors.NotFoundError as e:
        _report_not_found(e, e.response)


def _report_not_found(e, response):
    body = json.loads(response.read())
    logging.info(body["cause"])
    raise errors.ContainerNotFound(body["message"]) from e


__ALL__ = [
    "list_containers",
    "inspect",
    "kill",
]
