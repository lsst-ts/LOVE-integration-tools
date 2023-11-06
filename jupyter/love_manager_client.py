# This file is part of ts_externalscripts
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

__all__ = ["LoveManagerClient"]

import asyncio
import json
import logging

import aiohttp
from lsst.ts import salobj, utils


class LoveManagerClient:
    """Connect to a LOVE-manager instance.

    Parameters
    ----------
    location : `str`
        Host of the running LOVE-manager instance
    username: `str`
        LOVE username to use as authenticator
    password: `str`
        Password of the choosen LOVE user
    event_streams: `dict`
        Dictionary whith each item as <CSC:salindex>: <events_names_tuple>
        e.g. {"ATDome:0": ('allAxesInPosition', 'authList',
        'azimuthCommandedState', 'azimuthInPosition', ...)
    telemetry_streams: `dict`
        Dictionary whith each item as <CSC:salindex>: <telemetries_names_tuple>
        e.g. {"ATDome:0": ('position', ...)

    Notes
    -----
    **Details**

    * Generate websocket connections using provided credentials
    by token authentication and subscribe to every
    event and telemetry specified.
    """

    def __init__(
        self,
        location,
        username,
        password,
        event_streams,
        telemetry_streams,
        msg_tracing=False,
    ):
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        self.username = username
        self.event_streams = event_streams
        self.telemetry_streams = telemetry_streams

        self.token = None
        self.websocket_url = None
        self.command_url = None
        self.__api_headers = None

        self.__msg_tracing = msg_tracing
        self.num_received_messages = 0
        self.msg_traces = []

        self.__location = location
        self.__password = password
        self.__websocket = None

        self.start_task = utils.make_done_future()

    async def __request_token(self):
        """Authenticate on the LOVE-manager instance
        to get an authorization token and set the
        corresponding websocket_url.

        Raises
        ------
        RuntimeError
             If the token cannot be retrieved.
        """
        url = f"http://{self.__location}/manager/api/get-token/"
        data = {
            "username": self.username,
            "password": self.__password,
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=data) as resp:
                    json_data = await resp.json()
                    token = json_data["token"]
                    self.websocket_url = (
                        f"ws://{self.__location}/manager/ws/subscription?token={token}"
                    )
                    self.__api_headers = {
                        "Authorization": f"Token {token}",
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    }
                    self.command_url = f"http://{self.__location}/manager/api/cmd/"
            except Exception as e:
                raise RuntimeError("Authentication failed.") from e

    async def __handle_message_reception(self):
        """Handles the reception of messages."""
        if self.__websocket:
            async for message in self.__websocket:
                if message.type == aiohttp.WSMsgType.TEXT:
                    msg = json.loads(message.data)
                    self.log.debug("Received message: ", msg)
                    if "category" not in msg or (
                        "option" in msg and msg["option"] == "subscribe"
                    ):
                        continue
                    if self.__msg_tracing:
                        self.num_received_messages += 1
                        tracing = msg["tracing"]
                        tracing["client_rcv"] = utils.current_tai()
                        self.msg_traces.append(tracing)

    async def __subscribe_to(self, csc, salindex, topic, topic_type):
        """Subscribes to the specified CSC stream in order to
        receive LOVE-producer(s) data

        Parameters
        ----------
        csc : `str`
            Name of the CSC stream
        salindex: `int`
            Salindex of the CSC stream
        topic: `str`
            Topic of the CSC stream
        topic_type: `str`
            Type of topic: `event` or `telemetry`
        """
        subscribe_msg = {
            "option": "subscribe",
            "category": topic_type,
            "csc": csc,
            "salindex": salindex,
            "stream": topic,
        }
        await self.__websocket.send_str(json.dumps(subscribe_msg))

    async def start_ws_client(self):
        """Start client websocket connection"""
        try:
            await self.__request_token()
            if self.websocket_url is not None:
                async with aiohttp.ClientSession() as session:
                    self.__websocket = await session.ws_connect(self.websocket_url)
                    for name in self.event_streams:
                        csc, salindex = salobj.name_to_name_index(name)
                        for stream in self.event_streams[name]:
                            await self.__subscribe_to(csc, salindex, stream, "event")
                    for name in self.telemetry_streams:
                        csc, salindex = salobj.name_to_name_index(name)
                        for stream in self.telemetry_streams[name]:
                            await self.__subscribe_to(
                                csc, salindex, stream, "telemetry"
                            )
                    await self.__handle_message_reception()
        except Exception as e:
            raise RuntimeError("Manager Client connection failed.") from e

    async def send_sal_command(self, csc, salindex, cmd_name, params):
        """Send a SAL command to the specified CSC

        Parameters
        ----------
        csc : `str`
            Name of the CSC stream
        salindex: `int`
            Salindex of the CSC stream
        cmd_name: `str`
            Name of the command to be sent
        params: `dict`
            Parameters of the command to be sent
        """
        data = {
            "csc": csc,
            "salindex": salindex,
            "cmd": cmd_name,
            "params": params,
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.command_url, data=json.dumps(data), headers=self.__api_headers
                ) as resp:
                    json_data = await resp.json()
                    self.log.info("Command sent: ", json_data)
                    if resp.status == 500:
                        raise RuntimeError("Server error from commander")
            except Exception as e:
                raise RuntimeError(e) from e

    def create_start_task(self):
        self.start_task = asyncio.create_task(self.start_ws_client())

    async def close(self):
        if self.__websocket:
            await self.__websocket.close()
