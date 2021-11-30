from bs4 import BeautifulSoup
import requests
import os
import shutil
import re

work_dir_path = "/home/ojas/coding/"
cc_platforms = ["codechef","codeforces","cses"]

alphabets = []
for i in range(0,26):
	alphabets.append(chr(i+65))
for i in range(0,26):
	alphabets.append(chr(i+97))

def name_str_uniform(name):
	cons_str = 0
	new_str = ""
	for n in name:
		if n not in alphabets:
			cons_str+=1
		else:
			if cons_str>0 :
				new_str+="_"
				cons_str = 0
			new_str+=n
	if (name[-1] not in alphabets):
		new_str+="_"
	return new_str

class files:
	def __init__(self,files_to_move,files_to_del):
		self.files_to_move = files_to_move
		self.files_to_del = files_to_del

	def move_to_dir(self,src_path,dest_path):
		for file in os.listdir(src_path):
			if os.path.isfile(src_path+file):
				if file in self.files_to_move:
					shutil.move(src_path+file,dest_path+"/"+file)

	def del_from_dir(self,src_path):
		for file in os.listdir(src_path):
			if os.path.isfile(src_path+file):
				if file in self.files_to_del:
					os.remove(src_path+file)


class coding_platform:

	def __init__(self,platform):
		self.platform = platform
		
	def codechef(self):
		print("Initiating "+self.platform[0]+"...")

		codechef = ["school/","easy/","medium/","hard/","challenge/","extcontest/"]
		files_to_move = []
		files_to_del = []

		for i in range(0,len(codechef)):
			print(codechef[i])

			soup = BeautifulSoup(requests.get("https://www.codechef.com/problems/" + codechef[i]).content, "html.parser")
			problem_name_elements = soup.find(id="primary-content").find_all("div", class_="problemname")

			for problem_element in problem_name_elements:
				problem_code = str(problem_element.find("a")).split("/")[2].split("\"")[0]
				problem_name = name_str_uniform(problem_element.find("b").text.strip())

				files_to_move.append(problem_name+".cpp")
				files_to_del.append(problem_name+".exe")

			cc = files(files_to_move,files_to_del)
			cc.move_to_dir(work_dir_path,work_dir_path+self.platform[0])
			cc.del_from_dir(work_dir_path)	

			print("Total questions found: "+str(len(files_to_move)))

			del files_to_del[:]
			del files_to_move[:]	
			del cc

	def codeforces(self):
		print("Initiating "+self.platform[1]+"...")

		files_to_move = []
		files_to_del = []
		for i in range(1,75):
			print("Page: "+str(i))

			soup = BeautifulSoup(requests.get("https://codeforces.com/problemset/page/" + str(i)).content,"html.parser")

			problem_names = soup.find_all("div", attrs={"style":"float: left;"})

			for problem_name in problem_names:
				name = problem_name.find("a")
				link = str(name).split("\"")[1]
				div = link.split("/")[-1]


				name = div+"_"+name_str_uniform(name.text.strip())


				files_to_move.append(name+".cpp")
				files_to_del.append(name+".exe")
				# print(name)	


			cc = files(files_to_move,files_to_del)
			cc.move_to_dir(work_dir_path,work_dir_path+self.platform[1])
			cc.del_from_dir(work_dir_path)

			print("Total questions found: "+str(len(files_to_move)))

			del files_to_del[:]
			del files_to_move[:]
			del cc

	def cses(self):
		print("Initiating "+self.platform[2]+"...")

		soup = BeautifulSoup(requests.get("https://cses.fi/problemset/").content,"html.parser")

		problem_names = soup.find_all("li", attrs={"class": "task"})

		files_to_move = []
		files_to_del = []
		for problem_name in problem_names:
			name = problem_name.find("a",href=True)

			link = str(name).split("\"")[1].split("/")[2] + "/" + str(name).split("\"")[1].split("/")[3]

			name = name_str_uniform(name.text.strip())

			files_to_move.append(name+".cpp")
			files_to_del.append(name+".exe")

			# print(name)
		
		cc = files(files_to_move,files_to_del)
		cc.move_to_dir(work_dir_path,work_dir_path+self.platform[2])
		cc.del_from_dir(work_dir_path)	

		print("Total questions found: "+str(len(files_to_move)))
		
		del files_to_del[:]
		del files_to_move[:]
		del cc			


cc = coding_platform(cc_platforms)
cc.codechef()
cc.codeforces()
cc.cses()