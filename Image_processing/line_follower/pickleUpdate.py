import pickle 
 
 
def read_file(): 
 
	f = open("travel.txt", 'rb') 
	while True: 
		try: 
			L = pickle.load(f) 
 
			print("Place", L[1], "\t\t Travellers :", 
				L[2], "\t\t Buses :", L[3]) 
 
		except EOFError: 
			print("Completed reading details") 
			break 
	f.close() 
 
 
def update_details(): 
 
	f1 = open("travel.txt", "rb+") 
	travelList = [] 
	print("For a example i will be updating only Buses details") 
	t_code = int(input("Enter the travel code for the updation: ")) 
	 
	while True: 
		try: 
			L = pickle.load(f1) 
			if L[0] == t_code: 
				buses = int(input("Enter the number Buses ...")) 
				L[3] = buses 
			travelList.append(L) 
		except EOFError: 
			print("Completed Updating details") 
			break 
			 
	f1.seek(0) 
	f1.truncate() 
	 
	for i in range(len(travelList)): 
		pickle.dump(travelList[i], f1) 
	else: 
		f1.close() 
 
 
print("update the file") 
update_details() 
read_file() 
