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


__all__ = ["SimulatorCamera"]

import asyncio
import numpy as np

from .. import exposure
from . import genericcamera


class SimulatorCamera(genericcamera.GenericCamera):

    def __init__(self, log=None):

        super().__init__(log=log)

        self.isLiveExposure = False
        self.maxWidth = 1024
        self.maxHeight = 1024
        self.topPixel = 0
        self.leftPixel = 0
        self.width = self.maxWidth
        self.height = self.maxHeight
        self.bytesPerPixel = 2
        self.imageBuffer = None

        self.shutter_time = 0.5  # Time to open/close shutter
        self.shutter_steps = 10  # steps on opening shutter
        self.use_shutter = False
        self.shutter_state = 0  # State of the shutter 0 = Closed, self.shutter_steps = Open

        self.exposure_time = 0.001
        self.exposure_steps = 10  # steps on exposing
        self.exposure_state = 0  # State of the exposure

        self.readout_time = 0.5  # Time to readout
        self.readout_steps = 10  # steps on reading out
        self.readout_state = 0  # State of the reading out

        self.exposure_task = None

        self.isbusy_lock = asyncio.Lock()

        self.shutter_open_start_event = asyncio.Event()
        self.shutter_open_finish_event = asyncio.Event()

        self.exposure_start_event = asyncio.Event()
        self.exposure_finish_event = asyncio.Event()

        self.shutter_close_start_event = asyncio.Event()
        self.shutter_close_finish_event = asyncio.Event()

        self.readout_start_event = asyncio.Event()
        self.readout_finish_event = asyncio.Event()

        self.expose_count = 0

    @staticmethod
    def name():
        """Set camera name.
        """
        return "Simulator"

    def initialise(self, config):
        """Initialise the camera with the specified configuration file.

        Parameters
        ----------
        config : str
            The name of the configuration file to load."""
        pass

    def getMakeAndModel(self):
        """Get the make and model of the camera.

        Returns
        -------
        str
            The make and model of the camera."""
        return "Simulator"

    def getValue(self, key):
        """Gets the value of a unique property of the camera.
        Parameters
        ----------
        key : str
            The name of the property.
        Returns
        -------
        str
            The value of the property.
            Returns 'UNDEFINED' if the property doesn't exist. """
        return super().getValue(key)

    async def setValue(self, key, value):
        """Set a unique property of the camera.

        Parameters
        ----------
        key : str
            The name of the property.
        value : str
            The value of the property."""
        key = key.lower()
        await super().setValue(key, value)

    def getROI(self):
        """Gets the region of interest.
        Returns
        -------
        int
            The top most pixel of the region.
        int
            The left most pixel of the region.
        int
            The width of the region in pixels.
        int
            The height of the region in pixels."""
        return self.topPixel, self.leftPixel, self.width, self.height

    def setROI(self, top, left, width, height):
        """Sets the region of interest.

        Parameters
        ----------
        top : int
            The top most pixel of the region.
        left : int
            The left most pixel of the region.
        width : int
            The width of the region in pixels.
        height : int
            The height of the region in pixels."""
        self.topPixel = top
        self.leftPixel = left
        self.width = width
        self.height = height

    def setFullFrame(self):
        """Sets the region of interest to the whole sensor.
        """
        self.setROI(0, 0, self.maxWidth, self.maxHeight)

    def startLiveView(self):
        """Configure the camera for live view.

        This should change the image format to 8bits per pixel so
        the image can be encoded to JPEG."""
        self.bytesPerPixel = 1
        self.isLiveExposure = True
        super().startLiveView()

    def stopLiveView(self):
        """Configure the camera for a standard exposure.
        """
        self.bytesPerPixel = 2
        self.isLiveExposure = False
        super().stopLiveView()

    async def startShutterOpen(self):
        """Start opening the shutter.

        Check that shutter_task is not running and schedule open_shutter task
        to the event loop.
        """
        tasks = [self.exposure_task,
                 self.shutter_open_start_event.wait()]

        for f in asyncio.as_completed(tasks):
            await f
            break

    async def endShutterOpen(self):
        """End opening the shutter.

        Check that shutter_task is running and await for it to finish.
        """
        tasks = [self.shutter_open_finish_event.wait(),
                 self.exposure_task]

        for f in asyncio.as_completed(tasks):
            await f
            break

    async def startShutterClose(self):
        """Start closing the shutter.

        Check that shutter_task is not running and schedule close_shutter task
        to the event loop.
        """
        tasks = [self.exposure_task,
                 self.shutter_close_start_event.wait()]

        for f in asyncio.as_completed(tasks):
            await f
            break

    async def endShutterClose(self):
        """End closing the shutter.

        If the camera does have a shutter then this should wait for
        the shutter to finishing closing.

        If the camera doesn't have a shutter then don't do anything.
        """
        tasks = [self.exposure_task,
                 self.shutter_close_finish_event.wait()]

        for f in asyncio.as_completed(tasks):
            await f
            break

    async def startTakeImage(self, expTime, shutter, science, guide, wfs):
        """Start taking an image or a set of images.

        Parameters
        ----------
        expTime : float
            The exposure time in seconds.
        shutter : bool
            Should the shutter be opened?
        science : bool
            Should the science/main sensor be used?
        guide : bool
            Should guider sensor be used?
        wfs : bool
            Should wave front sensor be used?
        """
        if self.exposure_task is not None and not self.exposure_task.done():
            raise RuntimeError("Exposure task running.")

        self.exposure_time = expTime
        self.use_shutter = shutter

        self.log.debug("Cleaning events.")
        self.shutter_open_start_event.clear()
        self.shutter_open_finish_event.clear()
        self.exposure_start_event.clear()
        self.exposure_finish_event.clear()
        self.readout_start_event.clear()
        self.readout_finish_event.clear()
        self.shutter_close_start_event.clear()
        self.shutter_close_finish_event.clear()

        async with self.isbusy_lock:
            self.exposure_task = asyncio.ensure_future(
                self.simulate_exposure())

        await super().startTakeImage(expTime=expTime,
                                     shutter=shutter,
                                     science=science,
                                     guide=guide,
                                     wfs=wfs)

    async def endTakeImage(self):
        """End take image or images.
        """
        await self.exposure_task

        self.exposure_task = None

    async def startIntegration(self):
        """Start integrating.
        """
        tasks = [self.exposure_task,
                 self.exposure_start_event.wait()]

        for f in asyncio.as_completed(tasks):
            await f
            break

        await super().startIntegration()

    async def endIntegration(self):
        """End integration.

        This should wait for the integration period to complete."""
        tasks = [self.exposure_task,
                 self.exposure_finish_event.wait()]

        for f in asyncio.as_completed(tasks):
            await f
            break

        await super().endIntegration()

    async def startReadout(self):
        """Start reading out the image.
        """
        tasks = [self.exposure_task,
                 self.readout_start_event.wait()]

        for f in asyncio.as_completed(tasks):
            await f
            break

        await super().startReadout()

    async def endReadout(self):
        """Start reading out the image.
        """
        tasks = [self.exposure_task,
                 self.readout_finish_event.wait()]

        for f in asyncio.as_completed(tasks):
            await f
            break

        image = exposure.Exposure(
            self.imageBuffer, self.width, self.height, {})
        return image

    async def simulate_exposure(self):
        """ This method will simulate all steps of exposure asynchronously,
        issuing events as each step goes on.
        """

        async with self.isbusy_lock:

            # Note that open shutter events will only be issued if shutter
            # is in use
            if self.use_shutter:
                self.log.debug("Open shutter.")
                await self.open_shutter()

            self.log.debug("Exposing.")
            await self.expose()

            # Note that close shutter events will only be issued if shutter
            # is in use
            if self.use_shutter:
                self.log.debug("Closing shutter.")
                await self.close_shutter()

            self.log.debug("Reading out.")
            await self.readout()

            self.log.debug("Done taking simulated exposure.")

    async def open_shutter(self):
        """ Mimics task of opening the shutter.
        """

        if self.shutter_state == self.shutter_steps:
            raise RuntimeError("Shutter already open.")
        elif self.shutter_state != 0:
            raise RuntimeError(f"Shutter state is {self.shutter_state}. "
                               f"Expected 0.")

        self.shutter_open_start_event.set()

        while self.shutter_state < self.shutter_steps:
            self.shutter_state += 1
            await asyncio.sleep(self.shutter_time/self.shutter_steps)

        self.shutter_open_finish_event.set()

    async def close_shutter(self):
        """ Mimics task of opening the shutter.
        """
        if self.shutter_state == 0:
            raise RuntimeError("Shutter already closed.")

        self.shutter_close_start_event.set()

        while self.shutter_state > 0:
            self.shutter_state -= 1
            await asyncio.sleep(self.shutter_time / self.shutter_steps)

        self.shutter_close_finish_event.set()

    def make_random_buffer(self):
        """ Random buffer"""
        buffer = np.random.randint(low=np.iinfo(np.uint8).min,
                                   high=np.iinfo(np.uint8).max,
                                   size=self.width * self.height,
                                   dtype=np.uint8)
        return buffer

    def make_constant_iterating_buffer(self):
        buffer = np.ones(shape=(self.width * self.height), dtype=np.uint8)

        buffer = (buffer + self.expose_count % 3) * 25 + 128
        return buffer

    def make_horizontal_gradient_buffer(self):
        x = np.linspace(0, 255, self.width)
        x, y = np.meshgrid(x, x)
        buffer = x.astype(np.uint8).flatten()
        return buffer

    def make_vertical_gradient_buffer(self):
        x = np.linspace(0, 255, self.width)
        x, y = np.meshgrid(x, x)
        buffer = y.astype(np.uint8).flatten()
        return buffer

    def make_diagonal_gradient_buffer(self):
        x = np.linspace(0, 255, self.width)
        x, y = np.meshgrid(x, x)
        if self.expose_count % 2 == 0:
            buffer = (0.5*x + 0.5*np.flipud(y)).astype(np.uint8).flatten()
            return buffer
        buffer = (0.5*x + 0.5*y).astype(np.uint8).flatten()
        return buffer

    async def expose(self):
        """ Mimics exposure."""
        imageByteCount = self.width * self.height * self.bytesPerPixel

        if self.exposure_state != 0:
            raise RuntimeError("Ongoing exposure.")

        if self.exposure_time > 0.:

            print('self.exposure_time', self.exposure_time, flush=True)
            print('self.bytesPerPixel', self.bytesPerPixel)
            self.expose_count += 1
            self.exposure_start_event.set()
            # buffer = self.make_random_buffer()
            # buffer = self.make_constant_iterating_buffer()
            # buffer = self.make_horizontal_gradient_buffer()
            # buffer = self.make_vertical_gradient_buffer()
            buffer = self.make_diagonal_gradient_buffer()

            print(f"pre-buffer.max={buffer.max()}, len={buffer.shape[0]}, min={buffer.min()}")
            print(buffer)
            buffer = buffer.astype(np.uint8)
            print(f"buffer.max={buffer.max()}, len={buffer.shape[0]}, min={buffer.min()}")
            print(buffer)

            # x = np.linspace(0, 100, self.width)
            # y = np.linspace(0, 255, self.height)
            # x, y = np.meshgrid(x, y)
            # buffer = x.astype(np.int8).flatten()
            # buffer = np.sqrt(np.where(x < 50, shade, 255) * np.where(y < 50, shade, 255))
            # buffer = buffer.astype(np.int16)
            # print(f'shade: {shade}, min:{buffer.min()}, max:{buffer.max()}')

            self.log.debug(f"expose: {self.exposure_time}s.")

            self.imageBuffer = buffer

            while self.exposure_state < self.exposure_steps:
                self.exposure_state += 1
                self.log.debug(
                    f"Exposure steps {self.exposure_state}/{self.exposure_steps}.")
                await asyncio.sleep(self.exposure_time / self.exposure_steps)

            self.exposure_finish_event.set()

        else:
            self.log.debug(f"Taking zero second exposure.")
            self.exposure_start_event.set()
            # imageByteCount = self.width * self.height * self.bytesPerPixel
            self.imageBuffer = np.zeros(self.width * self.height,
                                        dtype=np.uint16)
            self.exposure_state = self.exposure_steps
            self.exposure_finish_event.set()

    async def readout(self):
        """Mimic readout.
        """

        if self.readout_state != 0:
            raise RuntimeError("Ongoing readout!")
        elif not self.exposure_state == self.exposure_steps:
            raise RuntimeError(f"Exposure not completed! State {self.exposure_state}, "
                               f"expected {self.exposure_steps}.")

        self.readout_start_event.set()

        while self.readout_state < self.readout_steps:
            self.readout_state += 1
            await asyncio.sleep(self.readout_time / self.readout_steps)
        self.readout_finish_event.set()
        # Reset exposure state
        self.exposure_state = 0

        # Reset readout state
        self.readout_state = 0
