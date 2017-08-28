#!/usr/bin/python
import pygatt
import time
import sys
import datetime
import subprocess
import os

class downloader:
	compressed_audio = bytearray()
	device = None

	def state_changed(self,handle, event):
		# Handle the state changing
		return

	def download_ready(self,handle, event):
		# Send LED Off
		self.device.char_write_handle(0x0027, bytearray([00,00,00,0x64,00]))
		self.compressed_audio += event
		
		return
	
	def __init__(self):
		# Inputs: HCI Device, Device Address

		# Set device
		adapter = pygatt.GATTToolBackend(hci_device='hci1')
		adapter.start()
		# Connect to Cloudpets
		self.device = adapter.connect('7C:EC:79:E3:A5:04')
		print '[+] Connected to Cloudpets'
		# Create "Has state changed" subscriber
		# Get current state
		self.device.char_read_handle
		self.device.subscribe('aaddf75d-a95a-0000-0004-3ca499b74009',callback=self.state_changed)

		# START RECORDING AUDIO NOW
		self.device.char_write_handle(0x0012, bytearray([8,2]))
		print '[+] Recording started'		

		# Stop recording (after 40 seconds) by sending "play" to slot zero
		time.sleep(40)
		
		self.device.char_write_handle(0x0012, bytearray([8,01,00]))
		print '[+] Recording stopped'		
		# WE ARE NOT CAPTURING AUDIO ANYMORE, GET THE AUDIO QUICKLY!!

		# Send LED OFF (Testing if we can control it) (Doesn't look to work)
		#self.device.char_write_handle(0x0027, bytearray([1,00,00,0x64,00]))
		
		# Create "Audio Downloader" subscriber
		self.device.subscribe('aaddf75d-a95a-0000-0003-3ca499b74009',callback=self.download_ready)
		
		print '[+] Downloading recording'		
		# Pass "Send Audio" command to Cloudpets
		self.device.char_write_handle(0x0012, bytearray([2]))

		# Wait for state to change, lets speed this up
		time.sleep(60)
		
		# Save compressed audio to file. Lets do timestamps next
		timestamp = '{:%Y-%m-%d-%H:%M:%S}'.format(datetime.datetime.now())
		#print 'Timestamp: {:%Y-%m-%d-%H:%M:%S}'.format(datetime.datetime.now())
		file = open('audio/' + timestamp + '.au', 'w')
		file.write(self.compressed_audio)
		file.close()

		subprocess.call(["/bin/sh", "/root/Workspace/Which/cloudpets/decode.sh", timestamp])

d = downloader()
