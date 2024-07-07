import cookies
import queue
import threading
import time

TEST_THREAD_LIMIT = 1

class OJService:
    def __init__(self) -> None:
        self.__latestRegistrationNumber__ = -1
        self.__taskList__ = []
        self.__carInUse__ = False # use for wificar porj only, since there is only one car
        self.__taskWaitingQue__ = queue.Queue()

    def __getRId__(self):
        self.__latestRegistrationNumber__ += 1
        return self.__latestRegistrationNumber__

    def addTask(self, zID, codeFile, problemId=""): # add the judgement request in queue
        from time import time
        taskInfo = self.OJTask.TaskInfo()
        taskInfo.codeFile = codeFile
        taskInfo.problemId = problemId
        taskInfo.zID = zID
        taskInfo.time = time()
        taskInfo.rID = self.__getRId__()
        ojtask = self.OJTask(TaskInfo=taskInfo)

        ojtask.inQueue(self)

        return taskInfo
    
    def statrOJServer(self):
        for _ in range(TEST_THREAD_LIMIT):
            t = threading.Thread(target=self.judger) 
            t.start()

        t = threading.Thread(target=self.__loop__)
        return 


    def __loop__(self): # here, it is not necessary to use multi-treating. One car only.
        while(True):
            time.sleep(1)

    def judger(self): # no need to have treat lock, only one test treat
        while(True):
            currentTask = self.__taskWaitingQue__.get()
            currentTask.do()


    class testPoint: # in FUTURE
        def __init__(self) -> None:
            self.questionID = None


        def __readIOFiles__():
            
            return # return two file IO

        def do(self): # start testing
            
            return

    class OJTask:
        # class
        def __init__(self, TaskInfo) -> None:
            self.rID = TaskInfo.rID # registration number
            self.codeFile = TaskInfo.codeFile # python script, file name in FUTURE
            self.problemId = TaskInfo.problemId 
            self.status = TASK_INIT
            self.testPoints = [] # test points array, to save test result in FUTURE
            self.zID = TaskInfo.zID
            self.time = TaskInfo.time
            return
        
        def do(self):
            self.statusUpdate(TASK_RUNNING)
            print(f"start the judging task {self.rID}")
            # python sys call

            return # status code
        
        def inQueue(self, serverObj): # can't be called manually. Currently, by OJService.addtask()
            serverObj.__taskWaitingQue__.put(self)
            serverObj.__taskList__.append(self)
            self.statusUpdate(TASK_WAITING)
            return

        def checkTaskInfo(self):
            info = self.TaskInfo()
            info.codeFile = self.codeFile # need to convert in FUTURE
            info.rID = self.rID
            info.problemId = self.problemId
            info.status = self.status
            info.testPoints = self.testPoints
            info.zID = self.zID
            info.time = self.time
            return info
        
        def statusUpdate(self, status):
            self.status = status
            return

        class TaskInfo:
            def __init__(self) -> None: # convert an OJTask object to a brief description
                self.rID = None # registration number
                self.codeFile = None
                self.status = None
                self.problemId = None
                self.testPoints = None
                self.zID = None
                self.time = None
                return 

    @classmethod
    def __task_status_int2str__(cls, statusCodeInt):
        match statusCodeInt:
            case 0:
                return "Init"
            case 1:
                return "In queue"
            case 2:
                return "Running"
            case 3:
                return "Finished"
            case -1:
                return "Run error"
            case -2:
                return "No communication with The agent"
            case -3:
                return "Update Failed"
            case -4:
                return "Cannot onnect to server"
            case -100:
                return "Sys_error" # I don't know what happened as well. It is a bug
            case _:
                return "Unknown Status Code"

TASK_INIT = 0
TASK_WAITING = 1
TASK_RUNNING = 2
TASK_FINISHED = 3
TASK_ERR_1 = -1 # Return python error to the client
TASK_ERR_2 = -2 # Post Waring to Teacher
TASK_ERR_3 = -3 # Delete the task and warn the client
SYS_ERR_100 = -100 # System is Offline
SYS_ERR_101 = -101 # Cannot find task