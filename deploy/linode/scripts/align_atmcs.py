#!/usr/bin/env python
# This file is part of LOVE-integration-tools
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by Inria Chile and the LSST Project
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

__all__ = ["AlignATMCS"]

import asyncio
import re

import yaml

from lsst.ts import salobj

class AlignATMCS(salobj.BaseScript):
    """Aligns the ATMCS

    """

    def __init__(self, index):
        super().__init__(index=index, descr="Aligns the ATMCS")
        # approximate time to construct a Remote for a CSC (sec)
        self.create_remote_time = 15
        # time limit for each state transition command (sec);
        # make it generous enough to handle any CSC
        self.cmd_timeout = 10

    @classmethod
    def get_schema(cls):
        schema_yaml = """
            $schema: http://json-schema.org/draft-07/schema#
            $id: https://github.com/lsst-ts/ts_standardscripts/AlignATMCS.yaml
            title: AlignATMCS v1
            description: Configuration for AlignATMCS
            type: object
            properties:
              instrument_port:
                description: Port to which the M3 mirror will point to
                type: number
            required: []
            additionalProperties: true
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

            * instrument_port : ...

        Constructing a `salobj.Remote` is slow (DM-17904), so configuration
        may take a 10s or 100s of seconds per CSC.
        """
        self.log.info("Configure started")
        self.remote = salobj.Remote(domain=self.domain, name='ATMCS')
        self.instrument_port = config.instrument_port
        self.log.info(f"Configure finished, instrument_port={self.instrument_port}")

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
        self.log.info("Running AlignATMCS script")
        if not self.remote.start_task.done():
            self.log.info(f"Waiting for remote to be ready")
            await self.remote.start_task

            self.log.info(f"Setting instrument port to={self.instrument_port}")
            self.remote.cmd_setInstrumentPort.set(port=self.instrument_port)
            try:
                await self.remote.cmd_setInstrumentPort.start(timeout=self.cmd_timeout)
            except TimeoutError:
                self.log.error('cmd_setInstrumentPort timeout exceeded')


asyncio.run(AlignATMCS.amain())
