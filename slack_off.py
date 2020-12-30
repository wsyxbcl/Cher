import logging
import time

#TODO refine menu and interface

class Slack():
    def __init__(self, name, status=1, time_start=time.time(), time_last=0, parent=None):
        self.name = name
        self.status = status # 0, 1, 2, 3 for done, doing, trash and todo
        self.time_start = time_start
        self.time_last = time_last
        self.parent = parent
        
    def __str__(self):
        return "{self.name}, {self.time_last}".format(self=self)
    
    def get_time(self):
        return time.time() - self.time_start
    


def slack_ui(slack):
    """
    help (h), ls, suspend (s), done (d), todo (t), continue (c), branch (b)
    """
    print("    {}".format(slack))
    while True:
        c = input("   >>>")
        if c == 'help':
            print("    help (h), ls, status (s), done (d), todo (t), remove (rm), branch (b)")
        elif c == 'continue':
            pass
        elif c == 'status':
            print("    {}".format(slack))
            print("    time: {}".format(slack.get_time()))
        elif c == 'done':
            slack.status = 0
            return 0
        elif c == 'todo':
            slack.status = 3
            return 3
        elif c == 'remove':
            slack.status = 2
            return 2
        else:
            print("Unknown command")
            
        
def slack_vis():
    pass

def slack_analysis():
    pass

def main():
    print("Slack off system v0.0.1")
    slack_list = [] #TODO consider a database
    global sys_status
    sys_status = 4 # 1, 4 for runing and idle status
    print("IDLE status")
    while True:
        current_slack = Slack(name=input(">>> "))
        sys_status = 1
        slack_status = slack_ui( )
    #TODO idle time, system uptime

if __name__ == '__main__':
    main()