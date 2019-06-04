import sys
import datetime
f = open('C:\\GrasshopperToCloud\\commonfile.txt','w')
_packet = '{"message_id" : %d, "cursor_position": %d, "command" : "%s", "robot_time": "%s"}' % (4,cur_pos,command,datetime.datetime.utcnow().isoformat())
f.write(_packet)
f.close()
print(_packet)
a=None