#!/usr/bin/env python
# This file is part of LOVE-integration-tools.
#
# Copyright (c) 2023 Inria Chile.
#
# Developed by Inria Chile.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or at
# your option any later version.
#
# This program is distributed in the hope that it will be useful,but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.


__all__ = ["ToggleATDomeShutter"]


import asyncio
import re

import yaml

from lsst.ts import salobj


class ToggleATDomeShutter(salobj.BaseScript):
    """Toggles the ATDome shutter between fully open and closed.
    """

    def __init__(self, index):
        super().__init__(index=index,
                         descr="Toggles the ATDome shutter between fully open and closed.")
        # approximate time to construct a Remote for a CSC (sec)
        self.create_remote_time = 15
        # time limit for each state transition command (sec);
        # make it generous enough to handle any CSC
        self.cmd_timeout = 10

    @classmethod
    def get_schema(cls):
        schema_yaml = """
            $schema: http://json-schema.org/draft-07/schema#
            $id: https://github.com/lsst-ts/ts_standardscripts/ToggleATDomeShutter.yaml
            title: ToggleATDomeShutter v1
            description: Configuration for ToggleATDomeShutter
            type: object
            properties:
              azimuth:
                description: Just in case
                type: number
            required: []
            additionalProperties: false
        """
        return yaml.safe_load(schema_yaml)

    async def configure(self, config):
        """Configure the script.

        Specify the CSCs to command, and for each CSC,
        specify the desired summary state optionally the settings.

        Parameters
        ----------
        config : `types.SimpleNamespace`
            Configuration with one attribute:

            * azimuth : desired deg rotation of the ATDome

        Constructing a `salobj.Remote` is slow (DM-17904), so configuration
        may take a 10s or 100s of seconds per CSC.
        """
        self.log.info("Configure started")
        self.remote = salobj.Remote(domain=self.domain, name='ATDome')
        self.log.info(f"Remote created successfully")

    def set_metadata(self, metadata):
        """Compute estimated duration.

        Parameters
        ----------
        metadata : SAPY_Script.Script_logevent_metadataC
        """
        # a crude estimate; state transitions are typically quick
        # but we don't know how many of them there will be
        metadata.duration = 60

    async def run(self):
        """Run script."""
        self.log.info("Running script")
        if not self.remote.start_task.done():
            self.log.info(f"Waiting for remote to be ready")
            await self.remote.start_task
            try:
                self.log.info("Reading the shutter state")
                dropout = await self.remote.evt_dropoutDoorState.aget(timeout=30)
                main_door = await self.remote.evt_mainDoorState.aget(timeout=30)
            except TimeoutError:
                self.log.error("Timed out trying to aget shutter state")
                return

            if dropout.state == 1 and main_door.state == 1:
                self.log.info("Opening shutter")
                await self.remote.cmd_openShutter.start(timeout=30)
            else:
                self.log.info(f"Closing shutter")
                await self.remote.cmd_closeShutter.start(timeout=30)


asyncio.run(ToggleATDomeShutter.amain())
