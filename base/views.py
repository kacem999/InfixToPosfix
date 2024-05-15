from django.shortcuts import render
import json
# Create your views here.
listOfSyb = {
    '&': '∧',
    '|':'∨' ,
    '>' :'→' ,
    '=' :'↔' ,
    '!' : '¬'
}
noLogic = {'F': 'V','V': 'F'}
andLogic = {'VF': 'F','FV': 'F','FF': 'F', 'VV': 'V'}
orLogic = {'VF': 'V','FV': 'V','FF': 'F', 'VV': 'V'}
impLogic = {'VF': 'F','FV': 'V','FF': 'V', 'VV': 'V'}
equLogic = {'VF': 'F','FV': 'F','FF': 'V', 'VV': 'V'}
listLogic = {'¬': noLogic,'∧': andLogic,'∨': orLogic,'→': impLogic,'↔': equLogic}

sybo = ['¬','→','∨','∧','↔','(',')']
op = ['∨','∧','↔','→']
pro = ['∨','∧','¬']
Listofdict = []

ListofStates = {}
logicStatment = {}
# FNC TEST
#1/ P ∨ Q ↔ ¬P
#2/ ¬(¬P → Q ∨ R) ∨ (P → Q)
def change(input_text,dict):
    new_input = []
    for i in input_text:
        if i in dict:
            new_input += dict[i]
        else:
            new_input += i
    return new_input
def depile(stack,mylist):
    reStack = list(stack)
    reStack.reverse()
    counter =0
    for i,ch in enumerate(reStack):
        if ch == '(':
            counter +=1
            break
        elif ch in op :
            mylist.append(ch)
            counter +=1
        else:
            counter +=1
    reStack = reStack[counter:]
    reStack.reverse()
    stack = reStack
    return mylist,stack

def check_priority(stack,mylist):
    reStack = list(stack)
    reStack.reverse()
    counter =0
    for i, ch in enumerate(reStack):
        if ch == '(':
            break
        elif ch in pro:
            mylist.append(ch)
            counter += 1
    reStack = reStack[counter:]
    reStack.reverse()
    stack = reStack
    return mylist, stack
def Postfex_and_Arber(request):
    #############Convert Infex to Postfex#############
    infix = []
    inf = []
    stack = []
    list = []
    ListofProposition = []
    if request.method == 'POST':
        nb = str(request.POST.get('number1'))
        infix.extend(nb)
        inf = change(infix,listOfSyb)
        jump = False
        for i in range(len(inf)):
            if inf[i] not in sybo:
                if jump is False:
                    list.append(inf[i])
                else:
                    jump = False
            elif inf[i] == '(':
                stack.append(inf[i])
            elif inf[i] == '¬' and inf[i + 1] == '(':
                stack.append(inf[i])
            elif inf[i] == '¬' and inf[i + 1] not in sybo:
                list.append(inf[i + 1])
                list.append(inf[i])
                jump = True
            elif inf[i] in op:
                if inf[i] == '→' or inf[i] == '↔':
                    list, stack= check_priority(stack,list)
                    stack.append(inf[i])
                else:
                    stack.append(inf[i])
            elif inf[i] == ')':
                list, stack = depile(stack, list)
        if len(stack) != 0:
            for ch in reversed(stack):
                if ch != '(':
                    list.append(ch)
        stack.clear()
        #############create arber#############
        counter = 0
        for i in range(len(list)):
            if list[i] not in op and list[i]!= '¬':
                stack.append(list[i])
                if list[i] not in ListofProposition:
                    ListofProposition.append(list[i])
            elif list[i] in op:
                l,r = stack[-2:]
                stack = stack[:-2]
                stack.append(counter)
                Listofdict.append({'id':counter,'op':list[i],'right':r,'left':l})
                counter += 1
            elif list[i] == '¬':
                s = stack[-1]
                stack = stack[:-1]
                stack.append(counter)
                Listofdict.append({'id': counter, 'op': list[i],'direct':s})
                counter += 1
        request.session['ListofProposition'] = ''.join(ListofProposition)
        request.session.save()
        Listofdict_as_json = json.dumps(Listofdict)
        request.session['Listofdict'] = Listofdict_as_json
        request.session.save()
        Listofdict.reverse()
        context = {'result': "".join(list), 'result2': "".join(inf), 'result3': Listofdict, 'result4': ListofProposition }
    else:
        context = {'result': None, 'result2': None, 'result3': [], 'result4': []}
    return render(request, 'base/result.html', context)

def CalcLogicStatment(left,right,op,Id):
    input = "".join([left,right])
    Logic = listLogic[op][input]
    NewLogic = {Id: Logic}
    return NewLogic

def evaluation(request):
    ListofPropo = list(request.session.get('ListofProposition', []))
    Listofdict_as_json = request.session.get('Listofdict', [])
    Listofdic = json.loads(Listofdict_as_json)
    if request.method == 'POST':
        print(ListofPropo)
        for ch in ListofPropo:
            state = str(request.POST.get(ch)) #state -> V or F
            ListofStates.update({ch: state}) #Ex : {p: V}
        for dict in Listofdic:
            if dict["op"] == '¬' :
                if dict["direct"] in ListofStates.keys():
                    Logic = listLogic["¬"][ListofStates.get(dict["direct"])]
                    logicStatment.update({dict["id"]: Logic}) # Ex: {0, V}
                else:
                    Logic = listLogic["¬"][logicStatment[dict["direct"]]]
                    logicStatment.update({dict["id"]: Logic})
            elif dict["op"] == '∧':
                if dict["right"] not in ListofStates.keys() and dict["left"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'∧',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'∧',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] not in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'∧',dict["id"]))
                elif dict["left"] in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'∧',dict["id"]))
            elif dict["op"] == '∨':
                if dict["right"] not in ListofStates.keys() and dict["left"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'∨',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'∨',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] not in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'∨',dict["id"]))
                elif dict["left"] in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'∨',dict["id"]))
            elif dict["op"] == '→':
                if dict["right"] not in ListofStates.keys() and dict["left"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'→',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'→',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] not in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'→',dict["id"]))
                elif dict["left"] in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'→',dict["id"]))
            elif dict["op"] == '↔':
                if dict["right"] not in ListofStates.keys() and dict["left"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'↔',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'↔',dict["id"]))
                elif dict["left"] not in ListofStates.keys() and dict["right"] not in ListofStates.keys():
                    left = logicStatment[dict["left"]]
                    right = logicStatment[dict["right"]]
                    logicStatment.update(CalcLogicStatment(left,right,'↔',dict["id"]))
                elif dict["left"] in ListofStates.keys() and dict["right"] in ListofStates.keys():
                    left = ListofStates.get(dict["left"])
                    right = ListofStates.get(dict["right"])
                    logicStatment.update(CalcLogicStatment(left,right,'↔',dict["id"]))
        print(logicStatment.values())
        resultLogic = list(logicStatment.values())[-1]
        logicStatment.clear()
        context = {'result5': resultLogic}

    else:
        context = {'result5':{}}
    return render(request, 'base/evaluation.html', context)

