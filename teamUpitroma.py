strategy_name = 'Educate, Replicate, Manipulate'

def getScore(my_history, their_history):
	calculatedScore = 0
	for i in range(len(their_history)):
		if my_history[i] + their_history[i] in ['rs','sp','pr']:
			calculatedScore +=1
		elif their_history[i] + my_history[i] in ['rs', 'sp', 'pr']:
			calculatedScore -=1
	return calculatedScore

def beat(move):
	if move=='r':
		return 'p'
	if move == 'p':
		return 's'
	if move=='s':
		return 'r'

def lose(move):
	if move=='r':
		return 's'
	if move == 'p':
		return 'r'
	if move=='s':
		return 'p'
		


def basicStrat(my_history, their_history):#<6
	if their_history[-1]+my_history[-2] in ['rs','sp','pr']:#beat beatLastMove
		return lose(my_history[-1])
	elif(their_history[-1]==their_history[-2]):# beat repeating
		return beat(their_history[-1])
	else:
		return beat(their_history[-1])#beat last move

def intermediateStrat(my_history, their_history):#<=10
	if (their_history[-1]+my_history[-2] in ['rs','sp','pr']) and (their_history[-2]+my_history[-3] in ['rs','sp','pr']):#beat confidant beatLastMove
		return lose(my_history[-1])
	elif (their_history[-1] == their_history[-3]) and (their_history[-2] == their_history[-4]):#beat confidant alternating
		return beat(their_history[-2])
	elif(their_history[-1]==their_history[-2]==their_history[-3]==their_history[-4]):# beat confidant repeating
		return beat(their_history[-1])
	elif (their_history[-1] == their_history[-4]) and (their_history[-2] == their_history[-5]):#looping by 3
			return beat(their_history[-3])
	else:
		return basicStrat(my_history, their_history)

def advancedStrat(my_history, their_history):#>10
	calculatedScore = 0
	beatLastConfidence = 0
	repeatingConfidence = 0
	alternatingConfidence = 0
	loopingConfidence = 0
	beatBeatLastConfidence = 0
	copyConfidence = 0
	looping4Confidence = 0

	

	#analyse opponent
	for i in range(len(their_history)):
		#score
		if my_history[i] + their_history[i] in ['rs','sp','pr']:
			calculatedScore +=1
		elif their_history[i] + my_history[i] in ['rs', 'sp', 'pr']:
			calculatedScore -=1

		if i>10:
			#beat last move
			if their_history[i]+my_history[i-1] in ['rs','sp','pr']:
				beatLastConfidence+=1
			else:
				beatLastConfidence-=1
			
			#repeating
			if their_history[i]==their_history[i-1]:
				repeatingConfidence+=1
			else:
				repeatingConfidence-=1

			#alternating
			if (their_history[i] == their_history[i-2]) and (their_history[i-1] == their_history[i-3]):
				alternatingConfidence+=1
			else:
				alternatingConfidence-=1

			#looping
			if (their_history[i] == their_history[i-3]) and (their_history[i-1] == their_history[i-4]) and (their_history[i-2] == their_history[i-5]):
				loopingConfidence+=2 #weighted
			else:
				loopingConfidence-=2
			
			#beat beat last move
			if their_history[i-1]+their_history[i] in ['rs','sp','pr']:
				beatBeatLastConfidence+=1
			else:
				beatBeatLastConfidence-=1

			#copy
			if their_history[i] == my_history[i-1] and their_history[i-1] == my_history[i-2]:
				copyConfidence+=1
			else:
				copyConfidence-=1

			#looping 4
			if (their_history[-1] == their_history[-5]) and (their_history[-2] == their_history[-6]):
				looping4Confidence+=1
			else:
				looping4Confidence-=1

	
	#determine opponent's strategy and counterattack
	opponentStratProb = {"beatLast":beatBeatLastConfidence, "repeating":repeatingConfidence, "alternating":alternatingConfidence, "looping":loopingConfidence, "beatBeatLast":beatBeatLastConfidence, "copy":copyConfidence, "looping4":looping4Confidence}

	opponentStrat = max(opponentStratProb, key=opponentStratProb.get)

	if(calculatedScore<(len(their_history)/4)):
		#I am not doing well
		#analyse self for weaknesses

		loopingConfidence=0
		if (my_history[i] == my_history[i-3]) and (my_history[i-1] == my_history[i-4]) and (my_history[i-2] == my_history[i-5]):
			loopingConfidence+=1
		else:
			loopingConfidence-=1

		alternatingConfidence = 0
		if (my_history[i] == my_history[i-2]) and (my_history[i-1] == my_history[i-3]):
			alternatingConfidence+=1
		else:
			alternatingConfidence-=1

		
		#modify self to cover weaknesses
		if loopingConfidence>len(my_history)/2:
			#I am looping
			return my_history[i-1]

		elif alternatingConfidence>len(my_history)/2:
			#I am alternating
			return beat(my_history[i])
		else:
			#I can't determine a weakness. Trying to throw them off
			if len(my_history)%5==0:
				return their_history[-1]
			else:
				return counterattack(opponentStrat,my_history,their_history)


	else:
		#I am winning. Carry on
		return counterattack(opponentStrat,my_history,their_history)
		




def counterattack(opponentStrat,my_history,their_history):
	if opponentStrat=="beatLast":
		return lose(my_history[-1])
	elif opponentStrat=="repeating":
		return beat(their_history[-1])
	elif opponentStrat=="alternating":
		return beat(their_history[-2])
	elif opponentStrat=="looping":
		return beat(their_history[-3])
	elif opponentStrat=="beatBeatLast":
		return their_history[-1]
	elif opponentStrat=="copy":
		return beat(my_history[-1])
	elif opponentStrat=="looping4":
		return beat(their_history[-4])
	else:
		intermediateStrat(my_history, their_history)
		


def move(my_history, their_history):
	
	if len(my_history)==0:
		return 'p'#guess

	elif len(my_history)==1:
		return beat(their_history[-1])#beat last move

	elif len(my_history)<=6:
		return basicStrat(my_history,their_history)
	elif len(my_history)<=10:
		return intermediateStrat(my_history,their_history)
	else:
		return advancedStrat(my_history,their_history)

		
