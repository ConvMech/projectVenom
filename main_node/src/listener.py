#!/usr/bin/env python
import rospy
import subprocess
import time
import os
import signal
import psutil
from std_msgs.msg import String

dir_save_bagfile = '/home/pi/bagfile/'

class start_stop:

	def terminate_process_and_children(self,p):
	  process = psutil.Process(p.pid)
	  print(p.pid)
	  for sub_process in process.children(recursive=True):
	      print("asking process to stop, pid:")
	      print(sub_process.pid)
	      #os.kill(sub_process.pid, signal.SIGTERM)
	      sub_process.send_signal(signal.SIGINT)
	     
	  p.communicate()
	  print("finished exiting!")

	def terminate_ros_node(self,s):
	    list_cmd = subprocess.Popen("rosnode list", shell=True, stdout=subprocess.PIPE)
	    list_output = list_cmd.stdout.read()
	    retcode = list_cmd.wait()
	    assert retcode == 0, "List command returned %d" % retcode
	    for str in list_output.split("\n"):
		if (str.startswith(s)):
		    os.system("rosnode kill " + str)

	def callback(self,data):
	    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

	    if (data.data == "record"):
		self.rosbag_process = subprocess.Popen('bash /home/pi/bash_script/bag_shell',shell=True)
		#time.sleep(5)
		print(self.rosbag_process.pid)
		print("successfully started the node! without camera")
                subprocess.Popen(['python', 'sound.py', 'no_cam_start.mp3'],cwd = "/home/pi/voice/")

            elif (data.data == "record_cam"):
                self.rosbag_process = subprocess.Popen('bash /home/pi/bash_script/bag_shell_cam',shell=True)
                #time.sleep(5)
                print(self.rosbag_process.pid)
                print("successfully started the node! including camera")
                subprocess.Popen(['python', 'sound.py', 'with_cam_start.mp3'],cwd = "/home/pi/voice/")

	    elif (data.data == "stop"):
	        subprocess.Popen(['python', 'sound.py', 'standby.mp3'],cwd = "/home/pi/voice/")
                self.terminate_ros_node("/record")
        	time.sleep(2)
		self.terminate_process_and_children(self.rosbag_process)
                subprocess.Popen(['python', 'sound.py', 'stop_complete.mp3'],cwd = "/home/pi/voice/")	    
	def listener(self):
            subprocess.Popen(['python', 'sound.py', 'init.mp3'],cwd = "/home/pi/voice/")
	    rospy.init_node('listener', anonymous=True)
	    rospy.Subscriber("chatter", String,self.callback)
	    rospy.spin()

if __name__ == '__main__':
    s = start_stop()
    print("node started")
    s.listener()


