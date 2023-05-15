#!/usr/bin/python3
import aditofpython as tof
import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(prog=__file__)

parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output. This will print additional debug information to stdout')
mode_group = parser.add_mutually_exclusive_group()
mode_group.add_argument('-n', '--near', action='store_false', help='Configures the camera to  "near" mode (default)')
mode_group.add_argument('-m', '--medium', action='store_true', help='Configures the camera to "medium" mode')
args = parser.parse_args()

system = tof.System()

mode = 'near'
if args.medium:
	mode = 'medium'

if args.verbose:
	dprint = print
else:
	def dprint(*_, **__):
		pass


cameras = []
status = system.getCameraList(cameras)
dprint("system.getCameraList()", status)

camera1 = cameras[0]

modes = []
status = camera1.getAvailableModes(modes)
dprint("system.getAvailableModes()", status)
dprint(modes)

types = []
status = camera1.getAvailableFrameTypes(types)
dprint("system.getAvailableFrameTypes()", status)
dprint(types)

status = camera1.initialize()
dprint("camera1.initialize()", status)

camDetails = tof.CameraDetails()
status = camera1.getDetails(camDetails)
dprint("camera1.getDetails()", status)
dprint("camera1 details:", "id:", camDetails.cameraId, "connection:", camDetails.connection)

status = camera1.setFrameType(types[0])
dprint("camera1.setFrameType()", status)

assert mode in modes, f"Selected mode '{mode}' is not avaiable on this camera. Available modes: {modes}"
status = camera1.setMode(mode)
dprint("camera1.setMode()", status)

def normalize(arr: np.array, dtype=np.float32) -> np.array:
	"""
	Returns a normalized copy of the given array (rescales all values to 0..1).
	By default the copy is of type np.float32.
	"""
	arr = arr.astype(dtype)
	arr -= np.min(arr)
	arr /= np.max(arr)
	arr = np.clip(arr, 0, 1)
	return arr


def toJet(arr: np.array, invalidBlack: bool = True, dtype=np.uint8) -> np.array:
	"""
	Converts a depth image to rgb by using the jet color scheme.
	"""
	arr = normalize(arr)

	# create the color image
	jet = np.zeros((arr.shape[0], arr.shape[1], 3), dtype=dtype)
	jet[:, :, 0] = np.clip(4 * arr - 1.5, 0, 1.0) * 255
	jet[:, :, 1] = np.clip(4 * np.abs(arr - 0.5) - 1.5, 0, 1.0) * 255
	jet[:, :, 2] = np.clip(-4 * arr + 2.5, 0, 1.0) * 255

	if invalidBlack:
		jet[arr==1] = (0, 0, 0)

	return jet

while True:
	frame = tof.Frame()
	status = camera1.requestFrame(frame)
	dprint("camera1.requestFrame()", status)

	frameDetails = tof.FrameDetails()
	status = frame.getDetails(frameDetails)
	dprint("frame.getDetails()", status)
	dprint("frame details:", "width:", frameDetails.width, "height:", frameDetails.height, "type:", frameDetails.type)

	#Depth
	depthImage = np.array(frame.getData(tof.FrameDataType.Depth), copy=False)
	depthImage = depthImage[0: frameDetails.height, 0: frameDetails.width]
	cv2.imshow('Depth', toJet(depthImage))
	dprint(depthImage)
	
	#Ir
	irImage = np.array(frame.getData(tof.FrameDataType.IR), copy=False)
	irImage = irImage[0: frameDetails.height, 0: frameDetails.width]
	cv2.imshow('IR', cv2.cvtColor((normalize(irImage) * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR))
	cv2.waitKey(1)