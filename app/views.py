import itertools

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import all_process, cal_process, process, avg_times

flag = 0
# Create your views here.
def about(request):
    return render(request, 'abb.html')

def algo(request):
    return render(request, 'algo.html')

def totalProcess(request):
    tp = request.POST['pNum']
    ap = all_process(t_p = tp)
    ap.save()
    return HttpResponseRedirect('/sim/')

def home(request):
    deleteAll(request)
    return render(request, 'home.html')

def sim(request):
    cDict = cal_process.objects.all()
    aDict = all_process.objects.all()
    p1Dict = process.objects.all()
    avgDct = avg_times.objects.all()
    print(avgDct.__str__)
    # tDict = time_quantum.objects.all()
    global flag
    if flag==1:
        flag=0
        pDict = process.objects.all().order_by("aT")
        return render(request, 'sim.html', {'pDict': pDict, 'cd': cDict, 'ad': aDict, 'avg': avgDct})
    
    newcon = {
        "temp": 0,
    }
    return render(request, 'sim.html', {'p1': p1Dict, 'cd': cDict, 'ad': aDict, 't': newcon, 'avg': avgDct})

def addProcess(request):
    try:
        newPID = request.POST['pID']
        newAT = request.POST['aT']
        newBT = request.POST['bT']
        newProcess = process(pID = newPID, aT = newAT, bT = newBT)
        newProcess.save()
    except:
        messages.success(request, "IntegrityError: CANNOT ENTER SAME PROCESS ID TWICE!")
        return HttpResponseRedirect('/sim/')
    return HttpResponseRedirect('/sim/')

# def addTQ(request):
#     newTQ = request.POST['tq']
#     newTqModel = time_quantum(tq = newTQ)
#     newTqModel.save()
#     return HttpResponseRedirect('/sim/')

def deleteProcess(request, proid):
    processTOdelete=process.objects.get(id=proid)
    processTOdelete.delete()
    return HttpResponseRedirect('/sim/')

def deleteAll(request):
    pr=process.objects.all()
    cal_pr=cal_process.objects.all()
    all_pr = all_process.objects.all()
    newavgt=avg_times.objects.all()
    newavgt.delete()
    # tq_pr = time_quantum.objects.all()
    # tq_pr.delete()
    all_pr.delete()
    cal_pr.delete()
    pr.delete()
    return HttpResponseRedirect('/sim/')

def cal_fcfs(request):
    # cal_pr=cal_process.objects.all()
    # cal_pr.delete()
    newavgt=avg_times.objects.all()
    newavgt.delete()

    y=[]
    for x in all_process.objects.all():
        y.append(x.t_p)
    total_process = y[0]
    p ={}
    for e in process.objects.all():
        a=[]
        a.append(e.aT)
        a.append(e.bT)
        p[e.pID] = a
    
    #print(p)
    p = sorted(p.items(), key=lambda item: item[1][0])
    print(p[0][0])
    ET = []
    for i in range(len(p)):
        # first process
        if(i==0):
            ET.append(p[i][1][1]+p[i][1][0])
    
        # get prevET + newBT
        else:
            if ET[i-1]>=p[i][1][0]:
                ET.append(ET[i-1] + p[i][1][1])
            else:
                ET.append(p[i][1][0] + p[i][1][1])
    
    TAT = []
    for i in range(len(p)):
        TAT.append(ET[i] - p[i][1][0])
    
    WT = []
    for i in range(len(p)):
        WT.append(TAT[i] - p[i][1][1])
    
    avg_WT = 0
    for i in WT:
        avg_WT +=i
    avg_WT = float((avg_WT/total_process))

    avg_TAT=0
    for i in TAT:
        avg_TAT+=i
    avg_TAT=float((avg_TAT/total_process))
    
    newAvgTime = avg_times(avg_proc_wt = avg_WT, avg_proc_tat = avg_TAT)
    newAvgTime.save()

    newAT=[]
    newBT=[]
    RT=[]
    for i in range(len(p)):
        RT.append(WT[i])
    
    print("Process | Arrival | Burst | Exit | Turn Around | Wait |")
    for i in range(total_process):
        newBT.insert(i,p[i][1][1])
        newAT.insert(i,p[i][1][0])
        newCalProcess = cal_process(cT = ET[i], tAT = TAT[i],  wT = WT[i], rt = RT[i])
        newCalProcess.save()
        print("   ",p[i][0],"   |   ",p[i][1][0]," |    ",p[i][1][1]," |    ",ET[i],"  |    ",TAT[i],"  |   ",WT[i],"   |  ")
    print("Average Waiting Time: ",avg_WT)
    print("Average Turn Around Time: ",avg_TAT)
    #print(cal_process.__str__(newCalProcess))
    k=0
    sm=0
    sm1=0
    print("Gantt Chart")
    while k<total_process:
        if k==0:
            sm += newBT[k]      
            print(newAT[k],"__P[",k+1, "]__", sm, end='')
        
        elif k>0:
            if newAT[k] > ET[k-1]:
                print("_NO_PROCESS_", end='')
                sm1=sm+newBT[k]       
                print("__P[", k+1, "]__",sm1, end='')
            else:
                sm1=sm+newBT[k]       
                print("__P[", k+1, "]__",sm1, end='')
        k=k+1
    q = avg_times.objects.all()
    global flag
    flag=1
    hm=[1, 3, 4]
    return HttpResponseRedirect('/sim/', {'q': q, 'hm': hm})


def cal_sjf(request):
    # cal_pr=cal_process.objects.all()
    # cal_pr.delete()
    newavgt=avg_times.objects.all()
    newavgt.delete()

    y=[]
    for x in all_process.objects.all():
        y.append(x.t_p)
    total_process = y[0]
    p ={}
    for e in process.objects.all():
        a=[]
        a.append(e.aT)
        a.append(e.bT)
        p[e.pID] = a
    
    p = sorted(p.items(), key=lambda item: item[1][0])
    pid=[]
    at=[]
    bt=[]
    ct=[0]*total_process
    tat=[0]*total_process
    wt=[0]*total_process
    f=[0]*total_process
    rtime=[0]*total_process
    st=0
    tot=0
    avg_wt=0
    avg_tat=0

    #u=0
    for i in p:
        pid.append(i[0])
        at.append(i[1][0])
        #at.pop()
        bt.append(i[1][1])
        #bt.pop()
        #f.append(0)
        #u+=1
        
    print(at)
    while(True):
        c = total_process
        min = 999999
        if (tot == total_process):
            # total no of process = completed process loop will be terminated
            break
    
        #If i'th process arrival time <= system time and its flag=0 and burst<min That process will be executed first
        for i in range(total_process):
            if at[i] <= st and f[i] == 0 and bt[i] < min :
                min = bt[i]
                c = i
        print(ct, tat) 
        # //If c==n means c value can not update because no process arrival time< system time, so we increase the system time
        if c==total_process:
            st+=1
        else:
            rtime[c] = st - at[c]
            ct[c] = st + bt[c]
            st += bt[c]
            print(at[c])
            print(ct[c])
            tat[c] = ct[c] - at[c]
            wt[c] = tat[c] - bt[c]
            
            f[c] = 1
            tot+=1

    for i in range(total_process):
        avg_wt+=wt[i]
        avg_tat+=tat[i]
        newSjfProcess = cal_process(cT = ct[i], tAT = tat[i], wT = wt[i], rt = rtime[i])
        newSjfProcess.save()
    
    global flag
    flag = 1
    avg_wt=avg_wt/total_process
    avg_tat=avg_tat/total_process

    newAvgTime = avg_times(avg_proc_wt = avg_wt, avg_proc_tat = avg_tat)
    newAvgTime.save()

    print("avg waiting time:", avg_wt," avg turn around time:", avg_tat )

    q = avg_times.objects.all()
    return HttpResponseRedirect('/sim/', {'q': q})

def cal_srtf(request):
    # cal_pr=cal_process.objects.all()
    # cal_pr.delete()
    newavgt=avg_times.objects.all()
    newavgt.delete()
    y=[]
    for x in all_process.objects.all():
        y.append(x.t_p)
    total_process = y[0]
    p ={}
    for e in process.objects.all():
        a=[]
        a.append(e.aT)
        a.append(e.bT)
        a.append(e.bT)
        p[e.pID] = a

    p = sorted(p.items(), key=lambda item: item[1][0])

     # Start simulation at the first arrival.
    current_time = p[0][1][0]
    result = []
    ct=[0]*total_process
    fr=[]
    total_idle_time=0
    ct_list = []
    nextvalues =[]
    restime = []
    while True:
        if not p: break
        # Find the process with the shortest remaining time.
        next = 0
        # Adjust current time if CPU was idle.
        if p[next][1][0] > current_time:
            total_idle_time+=1
            current_time+=1
            #current_time = p[next][1][0]
        else:
            for i in range(1, len(p)):
                # This condition relies on the list being sorted.
                if p[i][1][0] > current_time:
                    break
                if p[i][1][2] < p[next][1][2]:
                    next = i
            # Simulate one unit of time at the time in case another p
            # arrives.
            p[next][1][2] -= 1
            if next not in nextvalues:
                nextvalues.append(next)
                fr.append(current_time)

            current_time += 1

            if p[next][1][2] == 0:
                ct[next] = current_time
                ct_list.append(current_time)
                result.append([p[next], ct[next], 0, 0])
                restime.append(fr[next]-p[next][1][0])
                p.pop(next)
                ct.pop(next)
                fr.pop(next)
                nextvalues.pop(next)
                # restime[next] = fr[next]-p[next][1][0]
                # for l in range(99):
                #     fr.pop(1)
    
    avg_wt=0
    avg_tat=0
    for i in range(len(result)):
        result[i][2] = result[i][1] - result[i][0][1][0] - result[i][0][1][1]
        result[i][3] = result[i][1] - result[i][0][1][0]
        avg_wt+=result[i][2]
        avg_tat+=result[i][3]
    
    avg_wt=avg_wt/len(result)
    avg_tat=avg_tat/len(result)

    newAvgTime = avg_times(avg_proc_wt = avg_wt, avg_proc_tat = avg_tat)
    newAvgTime.save()

    print(result)
    print("Avg WT:", avg_wt," Avg TAT:", avg_tat)
    result1 = sorted(result, key=lambda item: item[0][0])
    for i in range(len(result1)):
        newSrtfProcess = cal_process(cT=result1[i][1], tAT=result1[i][3], wT=result1[i][2], rt=restime[i])
        newSrtfProcess.save()
    
    
    max_completion_time=max(ct_list)
    global flag
    flag=1
    print((max_completion_time-total_idle_time)*(100)/(max_completion_time))

    q = avg_times.objects.all()
    return HttpResponseRedirect('/sim/', {'q': q})

def cal_rr(request):
    # newavgt=avg_times.objects.all()
    # newavgt.delete()
    cal_pr=cal_process.objects.all()
    cal_pr.delete()
    newTQ = int(request.POST['tq'])
    print(newTQ)
    #newTqModel = time_quantum(tq = newTQ)
    #newTqModel.save()

    flg=[]
    p ={}
    for e in process.objects.all():
        a=[]
        a.append(e.aT) #0 
        a.append(e.bT) #1
        a.append(e.bT) #2 remaining burst
        a.append(0) #3 completion time
        a.append(0) #4 waiting time
        a.append(0) #5 turn around time
        a.append(0) #6 response time
        flg.append(0)
        p[e.pID] = a

    p = sorted(p.items(), key=lambda item: item[1][0])
    
    # Start simulation at the first arrival.
    current_time = p[0][1][0]
    
    for i in itertools.cycle(range(len(p))):
        # Terminate if all p are done.
        
        if all(process[1][2] == 0 for process in p):
            break
        # Skip this process if it has not yet arrived or if it is completed.
        if p[i][1][0] > current_time or p[i][1][2] == 0:
            continue
        current_burst = min(p[i][1][2], newTQ)
        p[i][1][2] -= current_burst
        if  flg[i]==0:
            p[i][1][6] = current_time
            flg[i]=1
        
        current_time += current_burst
        if p[i][1][2] == 0:
            p[i][1][3] = current_time
    
    avg_wt=0
    avg_tat=0
    for i in range(len(p)):
        p[i][1][4] = p[i][1][3] - p[i][1][0] - p[i][1][1]
        p[i][1][5] = p[i][1][3] - p[i][1][0]
        p[i][1][6] -= p[i][1][0]
        avg_wt+=p[i][1][4]
        avg_tat+=p[i][1][5]
        rr_process = cal_process(cT=p[i][1][3], wT=p[i][1][4], tAT=p[i][1][5], rt=p[i][1][6])
        rr_process.save()
    
    print(p)

    avg_wt=avg_wt/len(p)
    avg_tat=avg_tat/len(p)
    newAvgTime = avg_times(avg_proc_wt = avg_wt, avg_proc_tat = avg_tat)
    newAvgTime.save()
    print("Avg WT:", avg_wt, " Avg TAT:", avg_tat)
    
    global flag
    flag=1

    q = avg_times.objects.all()
    return HttpResponseRedirect('/sim/', {'q': q})