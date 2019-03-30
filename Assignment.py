""" This script intend to solve the following problem :
    1-The river crossing problem
    2-The 12 coins problem
    3-
    Author : Fangnikoue K. Ayao
    Date created : 2017/06/27
    Contact : malevae@gmail.com
"""
import sys, random, re
sys.path.append("module")
from e_object import e_object
from e_array import e_array
from time import sleep
from multiprocessing import Process
from e_console import Console
from itertools import repeat
from functools import reduce


class MissionaryCarnibal(e_object):
	
	def __init__(self,missions,carnis):
		super().__init__()
		#set total carnibal number to 0
		self.number_of_carnibal=carnis 
		#set total missionary number to 0
		self.number_of_missionary=missions
		#initialize an array to hold the number of carnibal,number of missionary and the boat position on the goal stage
		self.final_state = State((0,0,0))
		#initialize an array to hold the number of carnibal,number of missionary and the boat position in the initial stage
		self.initial_state = State((carnis,missions,1))

		"""
		initialization of number of trip carried by the boat
		"""
		self.boat_trip=0

		self.boat_capacity=2 #total number of object the boat can carry

		self.linked_list=[]#set the list of state node as a tree

		self.current_root_node=0#set this variable to the upper node index

		self.previous_state=[]#intialize the list of state previoulsy check by the search algorithm

		self.previous_state.append(self.initial_state)#set the first node with the initial state of the problem

		"""This variable hold all the successfully states that 
                   represent the next node to visit
		"""

		self.legal_previous_state=State()#simple intialize this object to empty state

		self.solution=e_array()#added all successfuly state to this object

		
		self.is_solution_found = False#Boolean object to hold the solution result


		"""This module hold all the successful state 
		   including those will be failed into the invalid state
		   near future.Use this object you can get all the path 
		   node executed by the search algorithm
		"""

		self.most_possible_solution=[]		

	"""
	The below method move either the number of carnibal or the number
	of missionary to the goal stage
	param1 'self' class object caller
	param2 'carnibal' number of carnibal to move
	param3 'missionary' number of missionary to move   	
	"""
	#method to initiate the capacity of the boat
	def boat_capacity(self,boat_capacity):

		self.boat_capacity=boat_capacity		

	"""method that append all the nodes to the 
	  linked_list object
	  Parameter: State class object

	"""

	def node_list(self,state):

		self.linked_list.append(state)


	"""Method declare to mode carnibal 
	   and missionaries to the other side 
	  of the river

	  Parameter1 : number of carnibal to move
	  Parameter2 : number of missionary to move
	"""		

	def move_to_final_stage(self,carnibal,missionary):

		self.final_state.carnis+=carnibal#add the request carnibal number to move to the existing carnibal number in the goal stage
		self.final_state.missions += missionary#add the request missionary number to move to the existing missionary number in the goal stage
		self.final_state.boat_pos = 1#set the boat position to the goal stage
		self.initial_state.carnis-=carnibal#delet the number of carnibal moved to the goal stage from the initial stage
		self.initial_state.missions-=missionary#delet the number of missionary moved to the goal stage from the initial stage
		self.initial_state.boat_pos=0#remove the boat from the initial stage

	"""The below method move either the number of carnibal or the number of
   	missionary from the goal stage to the initial stage
   	Parameter1: number of carnibal to move
   	Parameter2: number of missionary to move
	"""
	
	def move_to_initial_stage(self,carnibal,missionary):
	
		self.initial_state.carnis += carnibal#add the request carnibal number to move to the existing carnibal number in the initial stage
		self.initial_state.missions += missionary#add the request missionary number to move to the existing missionary number in the initial stage
		self.initial_state.boat_pos=1#set the boat position to the initial stage
		self.final_state.carnis-=carnibal#delet the number of carnibal moved from the goal stage
		self.final_state.missions-=missionary#delet the number of missionary moved from the goal stage
		self.final_state.boat_pos=0#remove the boat from the goal stage
	
	
	#simple printing message on the screen
	def void_message(self,*message_text):
		print(message_text)
		pass

	#get the user input when called
	def get_user_input(self):
		#request the user to input the number of carnibal and save it to the property number_of_carnibal
		self.number_of_carnibal = int(input("Enter number of carnibal : "))
		#request the user to input the number of missionary and save it into the property number_of_missionary
		self.number_of_missionary = int(input("Enter number of missionary : "))		
		#initialize the number of carnibal in the initial stage
		self.initial_state.carnis=self.number_of_carnibal

		#initialize the number of missionary in the initial stage
		self.initial_state.missions=self.number_of_missionary

	#get the default number of missionary and carnibal when called

	#check if the boat can be used

	def not_reach_goal_state(self):

		if self.initial_state.carnis ==0 and self.initial_state.missions==0:
			return False
		else :
			return True

	#get the name of the coast where the boat actually is	
	def get_boat_position(self):

		"""check if the boat is in the initial stage
   	   	and return the name of the initial stage
		"""
		if self.initial_state.boat_pos==1:
			return "East Bank"
		else :
			return "Ouest Bank"

	"""Start moving the missionary and the carnibal from Ouest Bank to the 
	   East Bank of the river.
	   This searching method used only a nomal representation of the object
	   both on the Ouest/East Bank.

	"""

	def start_moving_mc(self):

		

		self.boat_trip+=1#increment the boat_trip object each time this method is called

		"""Checking if missionary and carnibal just arrive in initial 
		  stage.Or also if one of the carnibal already been move to the 		 goal stage or all the missionary being moved to the goal stage
		"""
		
		if(self.initial_state.carnis == self.number_of_carnibal and self.initial_state.missions == self.number_of_missionary and self.initial_state.boat_pos==1) or (self.initial_state.missions == self.number_of_missionary and self.initial_state.carnis == (self.number_of_carnibal - 1) and self.initial_state.boat_pos ==1) or (self.initial_state.missions==0 and self.initial_state.carnis==self.number_of_carnibal and self.initial_state.boat_pos==1):
			"""Everytime this condition has been meet 
			   move 2 carnibals to the goal stage
			"""

			self.move_to_final_stage(self.boat_capacity,0)

		elif (self.initial_state.missions == self.number_of_missionary and self.initial_state.carnis ==1 and self.initial_state.boat_pos==1) or (self.initial_state.carnis==(self.number_of_carnibal - 1 ) and self.initial_state.missions==(self.number_of_missionary -1 ) and self.initial_state.boat_pos==1):
			"""in case the above condition is not meet 
			   move 2 missionary to the goal stage

			"""

			self.move_to_final_stage(0,self.boat_capacity)	

		elif (self.initial_state.carnis==1 and self.initial_state.missions==1 and self.initial_state.boat_pos==1):
			"""Everytime there is only 1 carnibal and 1 missionary
			  and the boat is in the initial stage move them all to 
			  to the goal stage
			"""

			self.move_to_final_stage(1,1)

		elif (self.final_state.carnis==(self.number_of_carnibal -1 ) and self.final_state.missions==( self.number_of_missionary - 1) and self.initial_state.boat_pos==0):
			"""Everytime there 2 carnibal and 2 missionary and the 
			   boat in the goal stage move 1 carnibal and 1 
			   missionary to the initial stage
			"""

			self.move_to_initial_stage(1,1)

		elif (self.initial_state.missions==0 and self.initial_state.carnis==1):
			"""If there is only one carnibal in the initial stage
			   move 1 missionary from goal stage to initial stage
			"""

			self.move_to_initial_stage(0,1)

		else :
			"""anything else just move the carnibal
			   from goal stage to initial stage
			"""

			self.move_to_initial_stage(1,0)

	"""In this method we are checking every possibility
	   to accomplish a successful state for a reason of number of carnibal 
	   greater than number of missionary in other side of the river and also 	   in case the missionary exists and vise versa
	"""
	

	def invalid_state(self):

		is_invalid_state=False#variable holding the result of condition in which the state is it can be either true or false

		if(self.final_state.carnis > self.final_state.missions and self.final_state.missions != 0) or (self.initial_state.carnis > self.initial_state.missions and self.initial_state.missions != 0 ):
			is_invalid_state=True
		
		return is_invalid_state

	"""Return a name of the bank on the east
	"""
	
	def east_bank(self):

		return "East Bank"

	
	"""Return a name of the bank on the ouest
	"""
	def ouest_bank(self):

		return "Ouest Bank"

	
	
	"""here we start moving all the carnibals and the missionaries 
	   We are looping over the possible way to bring all the objects
	   to the East Bank.
	   if the goal is reach,in another word if all the carnibals
	   and missionaries were successfully moved, stop the loop
	   but if it happen that we encounter any invalid state break
	   loop

	"""
	def move_carnibal_and_missionary(self):
					

		while(self.not_reach_goal_state()):

			print(" initial state (Missions=> {0} and Carnibal=> {1})  final state (Mission=> {2} and Carnibal=> {3})".format(self.initial_state.missions,self.initial_state.carnis,self.final_state.missions,self.final_state.carnis))		
		
			#check if the current moving is invalid
			if self.invalid_state():

				break

			else	:
			#in case that the moving object are ok start moving				
				self.start_moving_mc()	

	"""show the number of missionaries and carnibals with their 
	   respective parent node and child node index
	   Parameter1 : State class object
	"""

	def show_solution(self,state):

		"""check if this state is part of the valid possible 
		   solution take by the search argorithm
		"""		
		if (state.possible_solution):
		
			print("Valid state but chiled node failed or child node is the goal state")
		
  		#print the state informations

		print("Missionary=> {0} Carnibal=>{1} Boat Position => {2} Parent Node=>{3} Node Name=>{4}".format(state.missions,state.carnis,state.boat_pos,state.parent_node,state.node_name))

			

	"""This method is similar to show_solution method 
	   but instead of taking a single state as a parameter
	   it take a list of states
	   Parameter1: list of State class object
	"""
	def print_solution(self,list_state):

		if (self.is_solution_found):
			
			print("Total number of level before solution was found [{}]".format(self.solution.size()))

			"""loop throught a list of state and call show_solution
		   	   method and parse the current index state as a 
			   parameter
			"""		
			for state in list_state:

				self.show_solution(state)
		else:
		    print("Cannot found a solution")


	"""This algorithm is used to found a possible 
           solution throught a state space.
	   Parameter1 : Boolean that check if the user want also 
			display some valid state that have a failed 
			child node that the algorithm ignore

	"""

	def bread_search(self,possible_move=False):

	#	is_solution_found = False#Boolean object to hold the solution result


		#initialize the root node to be the initial state
		self.linked_list.append(self.initial_state)

		#initialize the root node to be the initial state
		self.most_possible_solution.append(self.initial_state)

		"""check if the user requiere to view also all possible
		  successfull state but has some child node failed along the 		      way
		"""
		
		if(not (possible_move)):

			"""Let us start performing the searching
			   if the list of node is empty and also
			   we have found the goal state stop the loop
			"""
		
			while(len(self.linked_list) > 0 and (not self.is_solution_found)) :
			
				"""Get the first node from the list of
				   available node
				"""
				curState=self.linked_list[self.current_root_node]

				#remove the retrieve node from the list
				self.linked_list.remove(curState)

				
				#check if this state is the goal state
				if(curState.equal(self.final_state)):

					"""In case we have found the goal
					   state set the solution boolean 
					   object to true
					"""
					self.is_solution_found=True

					"""append the current state to the
					   list of solution found
					""" 				
					self.solution.append(curState)

				else:
					"""In case this state is not the
					   goal state but is part of the
					  valid state which also not a 
					  duplicate state append it to the
					  list of valid state found

					"""
					self.solution.append(curState)

					"""give the valid state to the
					   tri_state method to check if this
					   current state can also be extend
					   to further state for founding the 						
					   goal state
					"""
		
					self.tri_state(curState)

		
		else:
			"""This loop is similar to the above one but 
			   in condition that instead looking at only
			   a valid state that reach to the goal state
			   it help also to print all the valid state
			   either the one that has child that is invalid
			   or duplicate state or a goal state
			"""
			while(len(self.most_possible_solution) > 0 and (not self.is_solution_found)):
				#get the first node from the list
				curState=self.most_possible_solution[self.current_root_node]
				#once the node is retrieve remove it from the list

				self.most_possible_solution.remove(curState)

				"""check if this state is the goal state
				"""

				if(curState.equal(self.final_state)):
					"""If this state is the goal state
					   initiate the is_solution_found
					   to true.
					   append this state to the list
					   of available valid state found
					"""
					self.is_solution_found=True
					self.solution.append(curState)

				else:
					"""If this state is not the goal 
					   state so it is a valid state
					   so we can append it to the list
					   of availabe valid state found.
					   We also need to pass this current
					   state to the tri_state method for
					   further heuristic to found the
					   goal state
					"""
					self.solution.append(curState)
					self.tri_state(curState)

		#let us print all the state found
		self.print_solution(self.solution)

	"""use this method to generate the child node from the given
	   parent node.

	  Parameter1 : State class object as a parent node
	  Parameter2 : a vector object of carnibal and missionary
			this vector represent the possible move for reqiuere
			for the algorithm to use

	  Return : State class object 

	"""


	def generate_child_node_state(self,parent_state,vector_of_carnis_missions,node_index):						

		cur_state=State(vector_of_carnis_missions)#create a state object from the given vector of carnis and missions


	   	#set the child node index to be the parent node	
		cur_state.node_index=parent_state.node_index


		#intialize the current level of the tree with the parent node level
		cur_state.tree_level=parent_state.tree_level

		#initialize the size of the boat for the child node
		cur_state.boat_size=self.boat_capacity

		#initialize the total number of carnis to move from the Ouest Bank
		cur_state.nber_of_carnis=self.number_of_carnibal

		#initialize the total number of missions to move from the Ouest Bank
		cur_state.nber_of_missions=self.number_of_missionary

		#increment the node tree to one 
		cur_state.tree_level+=1

		#initialize this state node_index
		cur_state.node_index=node_index

		#get the parent node for this state ,visit this method for more information
		cur_state.get_parent_node_name()

		#get the current node name,visit this method for help
		cur_state.get_child_node_name()

		return cur_state


	"""This method is use to generate a vector that look like 
	   a state representation

	  Parameter1 : State class object
	  Parameter2 : possible move vector that represent the possible number
			of missionaries and carnibals to move

	  return : vector represent the state
	"""
	
	def get_state_as_vector(self,state,obj_poss_mov):

		"""Initialize the possible number of missionary and carnibals
		   to move
		"""

		pm_missions,pm_carnis=obj_poss_mov
		
	
		#check to see that this state does not have the boat
		if(state.boat_pos==0):

			"""If this state does not have the boat
			   we start additing the possible number
			   of carnibal to move from the other side
			   to the existing carnibal in this state
			   same as the missionary and at the end
		           when all the object were move from the 
			   other state we put the boat back to this 
			   state by setting the boat_pos to 1
			"""
			carnis=pm_carnis+state.carnis
			missions=pm_missions+state.missions
			boat_pos=1
		else:
			"""In case this state has the boat 
			   we start removing the possible number
			   of carnibal from the existing carnibal in
			   this state.We have set the boat_pos to 0
		           that indicate that the boat is not available
			"""
			carnis=state.carnis-pm_carnis
			missions=state.missions-pm_missions
			boat_pos=0

		#return the vector representing the state

		return (carnis,missions,boat_pos)

	"""This method check if the current 
           state will reach the goal state or 
	   has been lead to a dead end state or has 
           the state has been check previously
           if it can lead to the goal state we append 
           this state to the object linked_list of state
           we also make sure on the current node if the algorithm
           found that there is more that 1 node that can reach the goal
           state I set the state property possible solution to true
           meanning that there is another way to reach the goal state

	"""


	def is_valid_node_reach_goal_state(self,cur_state):
		"""check if this state can lead to the goal state
		   see the obtimize_state_node for help
		"""

		if(self.optimize_state_node(cur_state)):

			"""Check if this state parent node 
			   different that the previous state 
                           parent node store before
			"""

			if((self.legal_previous_state.parent_node!=cur_state.parent_node)):
				"""No the parent node are different 
                      		   let's go and append this state
				   to the list of available state node
				   add this state as a legal state to the
          			   object legal_possible_state
				"""
				self.linked_list.append(cur_state)
				self.legal_previous_state=cur_state
			else:
				"""In case this state parent node equal to the
				   to the previous legal state parent node
				   set this state property possible solution
                                   to boolean true by default this property
                                   is set to true mean not a possible solution
                                   we can also do more here but i just leave it 
                                   like that.
				"""
				cur_state.possible_solution=True



	"""This where all the magic about
	   the state space happen.
		
	  Parameter1 : State class object
	"""
	def tri_state(self,state):
		#initialize a number of object the boat can carry with boat_size
		state.boat_size=self.boat_capacity

		#generate all possible move for this state see generate_possible_move for more information
		state.generate_possible_move()


		#set the current index node to 1
		node_index=1

		"""In all possible move found start checking if the found state
		   can be use to lead to the goal state
		"""		
		for pm in state.possible_move:

			"""generate the child node with the given parent node,
			   possible vector move and the current index node
			   see det_child_node_by_parent for help
			"""
			cur_state=self.get_child_node_by_parent(state,pm,node_index)


			node_index+=1#increment the child node index by 1

		
			"""With all the checking listed above now it is a time
			   to check if really the current state fit the 
			   solution to this problem by checking the counstrain
			   to follow while solving this problem
			"""

			if(not cur_state.invalid_state()):

				"""No worry here just curious to see how many 
				   node this search algorithm travel by calling 
				   the class method set_tree_level
				   (see this method for more infromation)
				"""

				State.set_tree_level()
				
				"""Now that this state is valid/safe
				   let us check also if the current state has
			           previously been check.see found_in method
	 			   for more information
				"""

				if( not self.found_in(self.previous_state,cur_state)):
					
					"""In case this state has not been
					   check before check if this state 
                                           will have a child node to lead us to
                                           the goal state
					"""
					self.is_valid_node_reach_goal_state(cur_state)
					"""save this state into the 
					   most_possible_solution object
                                           to see the total number of valid 
					   state the search algorithm has found
					"""	
					self.most_possible_solution.append(cur_state)

				"""if there is no issue save this state to the
				   list of all valid visit state object
				"""

				self.previous_state.append(cur_state)

	"""This method only help to shurten the path child node implementation
	   if call it will generate the child state with the available parameter
	   Parameter1 : State class object
	   Parameter2 : possible mode vector
           Parameter3 : int value that represent this state index node
	   Return : class State object
	"""

	def get_child_node_by_parent(self,state,pm,node_index=1):

		#initialize a vector of state
		curState=self.get_state_as_vector(state,pm)

		#initialize a state class object
		cur_state=self.generate_child_node_state(state,curState,node_index)
		return cur_state


	"""The below method help to check if the node pass as argument child
	   node can lead to the goal state if this state child node can lead
  	   to the goal state return a boolean True ortherwise return False.
	   Using this method also can help to eliminate all those child node
           state that will be lead into a invalid state or a previoulsy visit 
           state.

	  Parameter1 : class state object

          return : Boolean
	"""

	def optimize_state_node(self,state):
	
		#set the state boat capacity
		state.booat_size = self.boat_capacity

		"""generate every possible move check this method
         	   for more information
		"""
		state.generate_possible_move()


		"""In every possible move, try to check if the state is valid 	   
		"""
		for pm in state.possible_move:
		#initialize the state with parent state and possible move
			cur_state=self.get_child_node_by_parent(state,pm)

			#check if this state is valid/not

			if(not cur_state.invalid_state()):

				"""Check if this state has been check before
				   return false otherwise return true
				"""
				if(not self.found_in(self.previous_state,cur_state)):		
					
					return True

			self.previous_state.append(cur_state)

		#if not of checking are valid return false
		return False

				

	"""This method is only use to check if a state has been found
	   in the list of recorded state , if so return true and break the loop
	   otherwise just return the original value of is_object_found 
	"""
	def found_in(self,list_object,object_to_found):

		is_object_found=False#hold the current result of the checking

		"""Loop throught all the list of state list_object and try to 
		   check if the object_to_found exists set is_object_found to
                   True and stop the loop
		"""
		for object_index in list_object:
			"""Check if the current state retrieve from the list of
			   state is equal to the state object we are looking for
			"""

			if object_to_found.equal(object_index):

				is_object_found=True

				break

		return is_object_found	

	
				 
"""This State class help to build the object of the state space
   of the missionary and carnibal problem.
"""
class State:

	#static variable to hold all valid visited node
	s_tree_level=0

	"""create a contructor of the state
	   Parameter1 : vector that represent the initial state
           Parameter2 : vector that represent the goal state
	"""
	def __init__(self,initial_state=(0,0,0),goal_state=(0,0,0)):

		"""Below assignment is used because of the vector passed
		   The first element in the this vector represent the 
		   carnibals,the second represent the missionaries and the third
		   represent the position of the boat
		"""
		self.carnis,self.missions,self.boat_pos=initial_state
	
		#total number of object that the boat can carry
		self.boat_size=None	

		#represent the level of node from parent to child
		self.tree_level=0

		#hold a vector of all possible move the object can take
		self.possible_move=[]

		#vector that represent the goal state we are looking for
		self.goal_state=goal_state

		#total number of missionaries request to travel
		self.nber_of_missions=None

		#total number of carnibals request to travel
		self.nber_of_carnis=None	

		#current node name for the child node
		self.node_name="Root"

		#current index name of the child
		self.node_index=1

		#current node name for the parent
		self.parent_node="Root"

		
		self.possible_solution=False	

	"""return the node name of the parent
	   this parent node is found by getting the current search node tree
	   index
	   return : String
	"""
		
	def get_parent_node_name(self):
		 
		self.parent_node="Root_"+str(self.tree_level)

		return self.parent_node

	"""return the node name of the child
           this child node name is found by appending the parent node name
           to the node_index value of the child node
           return : String
	"""

	def get_child_node_name(self):

		self.node_name=self.parent_node+"_"+str(self.node_index)

		return self.node_name


	"""compare the equality of 2 states true if the exist are equals
	   otherwise retrun false
           Parameter1 : class State object
	   return     : Boolean
	"""
	def equal(self,state):
		is_equal=False

		"""Compare the number of carnibals,missionaries and the boat
		   boat position value against the caller method and the
		   argument
		"""

		if(self.carnis==state.carnis and self.missions==state.missions and self.boat_pos==state.boat_pos):
			is_equal=True
		return is_equal

	"""class method to get the total number of current node
	   return : integer represent the total number of valid node search
	""" 
	@classmethod
	def get_tree_level(cls):
		return cls.s_tree_level

	#class  method to increment the total valid node visited
	@classmethod
	def set_tree_level(cls):
		cls.s_tree_level+=1

	"""This method is the heart of a state search space implementation
           it check all the constrains report by the problem.It return true
           if the call state is invalid otherwise return false
	   
	   return : Boolean
	"""

	def invalid_state(self):

		#represent the current property of the checking state		
		is_invalid_state=False

		"""initiate the current missionary when deduct the state 
		   missionary from the request travel missionary
		"""
		cur_missions=self.nber_of_missions - self.missions
	
		"""initiate the current carnibal when we deduct the state
		   carnibal from the request carnibal
		"""
		cur_carnis=self.nber_of_carnis - self.carnis

		#check if the state missionary is greater than 0
		has_missions=self.missions > 0

		#check if the state carnibal is greater than 0
		has_carnis = self.carnis > 0


		"""Check if the state carnibal is greater than the missionary
                   if this condition is true the carnibal will eat the
		   missionary 
		"""
		is_carnis_gtr_missions=self.carnis > self.missions

		#check if the state carnibal compute is lower than 0
		no_carnis = self.carnis < 0

		#check if the state missionary compute is lower than 0
		no_missions = self.missions < 0

		"""Check is the state carnibal is greater than the carnibal
		   request to travel
		"""
		is_state_carnis_gtr_trav_carnis=self.carnis > self.nber_of_carnis

		

		"""This is where all the magic take place.
                   1-check if the total number of
                     carnibal is greater than the total number of missionary
                     and if only the total number of missionary is greater
		     than 0

		   2-check if the total number of carnibal in this state is 
		     greater than the total number of carnibal request to travel

		   3-check if the total number of missionary in this state is
                     greater than the total number of carnibal request

		   4-check if the total number of carnibal in this state is 
                     lower than 0

                   5-check if the total number of missionary in this state is
                     lower than 0

                   6-check if the total number of carnibals in this state deduct
		     from the total number of carnibal request to travel greater
		     than the total number of missionary in this state deduct
		     from the total number of missionary request to travel
                     and also this sum is greater than 0 

		  if the above checking were matches mark this as invalid
		  otherwhise mark it as valid state
		"""
		

		if(is_carnis_gtr_missions and has_missions) or is_state_carnis_gtr_trav_carnis or (self.missions > self.nber_of_missions) or no_carnis or no_missions or (( cur_carnis > cur_missions) and ( cur_missions > 0) ):

			is_invalid_state=True 
			
		return is_invalid_state	

	#return the total size of number of person support by the boat
	def get_boat_size(self):
		return self.boat_size

	#initialize the total size(object that can be carry by boat) of the boat 
	def set_boat_size(self,boat_size):
		self.boat_size=boat_size


	"""this method check all possible move the algorithm
           can take to find the solution
	"""
	def generate_possible_move(self):

		"""With the total number of objects the boat can carry
		   add to 1 to make sure the length is include
		  Example : if the boat can carry only n object the total
                            size for our object will becode (n+1) for
                            the possible value to be 0 to n
		  i have initialize the first index to represent 
                  the first value of the vector and j the second value 
                  of the vector
                   
		"""
	

		for i in range((self.boat_size)+1):
			for j in range((self.boat_size)+1):
				"""let us make sure that the sum of i and j
                                   cannot surpass the size of the boat
                                   neither their sum cannot be different than 0
				"""
				if((i+j) <=self.boat_size) and ((i+j) !=0):
					"""If the condition is found assign
                                           i and j as an array to the possible 
                                           move object
					"""
					self.possible_move.append([i,j])	
	

"""This Coins class help to build and solve the 
   any coins problem
"""

class Coins(e_object):

	def __init__(self):
		super().__init__()

		#variable that hold the status of the search
		self.coins_found=False
		#initialize the array or list of a coins
		self.coins=e_array()
		#initialise coins group to check their weight
		self.coins_group=e_array()
		#declare to count the number of weighing
		self.number_of_weigthing=0
		#declare to hold the odd coins value
		self.odd_coins=0
		"""hold the coins when either the total number of the coins 
		   is not divisible by 3 or by 2
		"""
		self.coins_holder=0
		"""Boolean object that hold if there is coins left to review
		   later
		"""
		self.coins_in_hold=False
		"""object that hold a current good coins from one group
		   of coins after being check against each 2 others
                   Example consider a vector group of coins A,B,C and if A > B 
		   means either A=C or B=C and if then C[0] will represent the
                   the good_coins_holder
                    
		"""
		self.good_coins_holder=None
		#hold the current progress bar index of the search
		self.index=10
   		#hold all message to be print out to the screen
		self.m_verbose=[]

		"""set this object true to alert the system that there 
		   is request to check only 2 coins and if it happen the system
		   will not know which coin the user want to check so it will
                   display a prompt input for the user to choose.
		"""
		self.conterfait_checking=False

		#object hold the user input for the above statement
		self.check_conterfait=None

		self.starting_coins_size=0

		self.searching_attempt=0

		self.coins_group_holder=[]

		self.is_change_group_in_hold=False
		#number to divide the group of coins with
		self.divider=0

		self.same_coins=False
	
	"""called this function to check if the odd coins is found
           Parameter: void
           Return   : Boolean True if the odd coins is found and False otherwise
	"""

	def is_odd_coins_find(self):

		return self.coins_found

	"""start looking for the odd coins 
	   [Parameter1] : optional vector that hold all the coins
	   Return       : void

	"""
	def finding_coins(self,list_coins=[]):
		"""here we go we start looking for the odd coins by calling 
                   method.go this method for more information
		"""
		self.find_odd_coins(list_coins)

	""" Now we start searching for the odd coins

	    [Parameter1] : optional list of coins
	    Return 	 : void
	"""
	def find_odd_coins(self,list_coins=[]):
				
		#check if the list_coins object is not empty
		if(len(list_coins)>0):
			"""if this list is not empty loop through it and 
			   initiate the coins array object
			"""
			self.starting_coins_size=len(list_coins)

			for i in list_coins:
		
				self.coins.append(i)			

		print("Number of coins load %d "%self.coins.size())

		self.debug(message="Coins searching in progress")

		"""Now we have a work to do check if the odd coins is found
		"""	

		self.exec_time.start_time()

		while not self.is_odd_coins_find():
			#if the odd coins not found set the length of the coins

			len_coins=len(self.coins)

			#initialize for the progress bar
			sleep(0.1)

			"""this function help to perform the search of the 
			   odd coins see this method for details
			"""
			self.search_coins()

			#if (self.index + 2 > 100):
				
			#	self.index-=20
					
			#start the progress bar
			self.progress_bar(self.index,100,"Progress:","Complete",50)
			#hide the cursor while displaying the progress
			Console.cursor.hide()
			#check if the odd coins is not found
			if (not self.coins_found):
				"""if it happen that the odd coins is 
				   not found scale the group  of the coins
				   see this method for more details
				"""		
				self.scale_coins()
			
			#increment the progress bar	
			self.index+=1

			self.searching_attempt+=1

			#if(len_coins==self.starting_coins_size and self.searching_attempt==13):
			#	self.index=100

			#check if the index is equal
			if(self.index == 100 and (not self.is_odd_coins_find())):
				self.coins_error()
				break
		#if odd coins found display the cursor back
		Console.cursor.show()
					
	"""simple use to print any message on the stdout
	   Parameter1 : key word argument
	   Return     : void
	"""
	def debug(self,**options):

		#display the argument option name message
		print("%s"%options.get("message"))

	def coins_error(self):
	
		self.debug(message="\nCannot determine the odd coins")
			

	"""display all saved verbose essage when call
	   Parameter : void
	   return    : void
	"""
	def verbose(self):

		if(self.same_coins):

			self.m_verbose=[]
			self.m_verbose.append("Cannot determine the odd coins")
			self.m_verbose.append("The coins are the same")

		else:
			#append this line into the m_verbose list
			self.m_verbose.append("odd coins is %s and total number of weigthing is %d"%(self.odd_coins,self.number_of_weigthing))
	
			#print a new line
			#print("\n")

		"""In every index found in the m_verbose object
                   print it to the stdout
		"""
		for i in range(len(self.m_verbose)):
			message=self.m_verbose[i]
			print(message)		
			

	"""this method can be use to initiate all the coins
	   Parameter1 : list that represent value of the odd coins to initiaze
			the value of all normal coins the total number of
                        the coins to initialize and the index in the list
                        that will old the odd coins
	"""
	def init_coins(self,*arg_list):

		self.debug(message="Loading coins please wait...")	

		"""
		  Parameter1 : the value of the odd coins
	  	  Parameter2 : the value represent all coins
    	  	  Parameter3 : total number of all coins given to search
	  	  Parameter4 : the place to put the odd coins
		"""

		odd_coins,coins_value,coins_total,odd_coins_index=arg_list

		"""in the total coins start initialize all the coins
		   because we know that n-1 contain all the good coins
                   only n-(n-1) that contain the conterfait coins either
                   heavier or lighter
		"""	

		self.starting_coins_size=coins_total	
		
		for i in range((coins_total)):

			#add the coins_value to the the rest of the coins list
			self.coins.append(coins_value)

		#add the conterfait coins to the desire index set by the user
		self.coins[odd_coins_index]=odd_coins

		#display a successfully message after coins were added
		self.debug(message="Coins successfuly load")

		loading_time="Loading time:(%s seconds)"%self.exec_time.diff_btwn_date_in_sec()

		self.debug(message=loading_time)

	"""divide the size of the current searching coins per group
	   Parameter1 : the number for which the coins will be divided to
	"""

	def divide_coins_in_group(self,divided):

		len_coins=len(self.coins)

		"""The number_of_coins_per_group hold the value of n/3 
		    with n the size of the coins means the total number
		   coins in each group
		"""
		number_of_coins_per_group=int(len_coins / divided)

		#initialize the number of group to divide the coins into			
		multiple_of_total_coins=int(len_coins/number_of_coins_per_group)

		j=0#current group index

		"""Loop through the number of group and starting divide the 
		   coins
		"""
		for i in range(multiple_of_total_coins):

			"""save the first group of the coins in the
			   coins_group object.assume 'I'=size of the coins / 
			   the number the group can be divided with
                           to find the group x and y is the list of the coins
                           and also z=0 is the first element in y so
                           x=[z:z+I] for 'K'=size of coins / 'I' with n < 'K'
			   for n+1 < 'K' then z=(z+I) 
			    
			"""
			self.coins_group.append(self.coins[j:j+number_of_coins_per_group])

			#increment j with the size of each group
			j+=number_of_coins_per_group
		

	"""this is were all the magic happen , use of this method
	   help to either divided the coins into 3 group first if the total 
	   number of all coins is divisible by 3 and greater than 3
	   or check if the total number of all coins is divisible by 2 
	   and greater than 2,or is the total number of the coins is equal to 2 
           or 3 eitherwise remove 1 coins from the total number of coins
           and go back to the above checking again.But in case the total number
           of all coins is either modulo 3 or 2 split the coins into 
           the respective group(3 or 2) and scale it.
	"""
	def search_coins(self):

	#	self.load_existing_coins_group()

		#set the size of the searching coins
		len_coins=len(self.coins)

		#print(self.coins)

		#variable that will hold the coins by group to scale
		self.coins_group=[]

		"""check if the size of the coins is divisible by 3 
		   or greater than 3 
		"""
		if (len_coins % 3.0 == 0 and len_coins > 3):

			"""get each group and save  each group in the
			   coins_group object.see below method for details
			"""
			self.divide_coins_in_group(3)

		elif (len_coins % 2.0 == 0 and len_coins > 2):

			self.change_group_size()
			if(self.is_change_group_in_hold):
				self.divide_coins_in_group(self.divider)

			
			"""get each group and save each group in 
			   the coins_group object.see below mehod 
			   for more details
			"""

		elif ( len_coins == 3 or len_coins == 2):

			i=0

			#check if size of the coins is 3 or coins is found

			if (len_coins==3 and (not self.coins_found)):
				#increment the weigthing value to 1

				self.number_of_weigthing+=1

				#see this method for more details
				self.found_odd_coins_in_tree()

			else:

				
				"""if the length of the size of the coins is
				   not equal to 3 then it is equal to 2
                                   so if it is check if the the coins with
                                   index 0 is greater than the coins in index
                                   1
				"""			
				if((self.coins[i] > self.coins[(i+1)]) and (not self.coins_found)):
					"""Check if there is any coins in
                                           holding and if not
					"""
					
					if(self.good_coins_holder==None):
						#initiate the coins checking to true

						self.conterfait_checking=True
						#we now need to increment the weighting
						self.number_of_weigthing+=1
						#if all ok we found the coins
						self.coins_found=True
					else:	
						#increment the weighting			
						self.number_of_weigthing+=1

						"""In this case we have other
						   coins in hold so call
                                                   found_odd_coins
						   (see this method for detail)
						   method		   
						"""
						self.found_odd_coins()
		
				else:
					"""in case the coins index 0 is not 
					   greater that the coins with index 1
					   check if there is any coins in hold
					"""

					if(self.good_coins_holder==None):
						"""untill here we can conclude
                                                   that the odd coins is found
                                                   and get the coins
						"""
						self.odd_coins=self.coins[i]

						#set this variable to true
						self.coins_found=True
					else:
						"""if the above statement is not
						   true check if there is no
						   coins in hold
						"""
						if(not self.coins_in_hold):
							"""If not just call
                                                           the below method
							"""	

							self.found_odd_coins()
						else:
							"""if there is load the
                                                           holding coins
							"""
							self.load_coins_in_hold()				
		else:
			"""in area if the size of the coins is not divisible by
                           3 nor by 2 and is not equal to 3 nor to 2 
                           we have to start doing other checking describe in the 			   below method check it for more details
			"""
			self.found_no_divisible_coins()
		
		"""called this method to check the weigthing of the coins we 
		   have found.Check this method out for more details 
		"""
		self.is_coins_heavier_or_lighter()

		
	#	self.load_existing_coins_group()

 
	"""
	   Parameter1 : represent which coins the user want to check
                        either the heavier one or the lighter one
                        if this parameter is 'heavier' the system will
                        show x for x=k[0] > k[1] for k the list represent
                        all the current coins.
	  Return      : void
	"""	
	def get_odd_coins_equal_scale(self,conterfait_weigh):
		"""Check whether the conterfait_weigh is 'lighter' or 'Enter'
                   and 
		"""
		if(conterfait_weigh=="lighter" or conterfait_weigh=="Enter"):
			#check which coins is greater than other
			if(self.coins[0] > self.coins[1]):
				return self.coins[1]
			else:
				return self.coins[0]
		else:
			#check which coins is greater than other
			if(self.coins[0] > self.coins[1]):
				return self.coins[0]
			else:
				return self.coins[1]

	def load_existing_coins_group(self):
		
		len_group_holder=len(self.coins_group_holder)

		if(len_group_holder > 0):	
		
			self.coins.append(self.coins_group_holder[0])


			if(len_group_holder > 1):
				self.coins.append(self.coins_group_holder[1])		    
		self.coins_group_holder=[]
	
	"""This method is only use to display a message by checking the 
	   weighting of the coins. with this message we check if the coins has
	   been found , and if so move on to check if there is any coin in hold
           and it is check if the coin in hold is lighter or heavier than the
           current coins and so on.
	"""
	def is_coins_heavier_or_lighter(self):
		#check if the odd coins has been found
		if(self.coins_found):
			"""if odd coins found set the progress index bar to 100
			   which mean terminate the progress bar.
			"""
			self.index=100

			#check if there is any coins in hold			
			if( self.good_coins_holder != None):
			
				#check if the odd coins is greater than the hold coins
				if(self.odd_coins > self.good_coins_holder):

					self.m_verbose.append("The odd coins is heavier")
				else:
					self.m_verbose.append("The odd coins is lighter")
			else:
				"""in case there is no coins in hold probaly the
				   user request only to check 2 coins
				   and in that case the system does not know 
				  which coins to display to the user so it will
                                  ask the user to choose either to display the
                                  heavier or lighter coins with a prompt line
                                  in case the user choose not to and press enter
                                  the system will only display the lighter coins
				"""
				#check if the conterfait_checking is set to true
				if (self.conterfait_checking):
					#verbose to the user what had happen

					print("The odd coins is either heavier or lighter,since we cannot predict it")
				
					#ask the user to choose in the coins
					Console.get_choice_input("Which conterfait you want to check lighter/heavier or press enter for default:",["lighter","heavier","Enter"])
					"""get the user input by calling the 
					   get_input_data Console class function
					   this input will now be pass to the
					   get_odd_coins_equal_scale(see this
					   method for more details)
					   as an 
					   argument
					"""
					self.odd_coins=self.get_odd_coins_equal_scale(Console.get_input_data())
			


	"""This method take the size of the coins x if x > 1 and remove the
           first value to and store it in coins_holder object to make the size
           of the coins either divisible by 3 or 2.
	"""
	def found_no_divisible_coins(self):
		
			i=0
			#is the coins size greater than 1 ?

			if (len(self.coins) > 1):
				#is there is no coins in hold ?
				
				if (not self.coins_in_hold):

					#get the first value from the coins list 
					self.coins_holder=self.coins[0]

					#set the coins_in_hold object to true			
					self.coins_in_hold=True

					#reset the coins group array
					self.coins_group=[]

					"""delete the value store in 
					   coins_holder object from the coins 
					   list
					"""
					del self.coins[0]
				else:
					"""append the coins_holder value to
					   the list of coins
					""" 
					self.coins.append(self.coins_holder)
					#reset the coins holder boolean object
					self.coins_in_hold=False
					

			else:
				#if there is no coin in hold
				if (not self.coins_in_hold):
					#set the odd coins value
					self.odd_coins=self.coins[i]
					#set coins found value
					self.coins_found=True
				else:
					"""Check if the coins value at index 0
					   in the list of the coins is greater
					   than the coins holder value if so
					   initialize the odd coins to the coins
					   holder value and set the coins found
					  object to true otherwise set the odd
					  coins to the first value in the coins
					  list and set the coins find to true
					"""
					if(self.coins[0] > self.coins_holder):
						self.number_of_weigthing+=1
						self.odd_coins=self.coins_holder
						self.coins_found=True
					else:
						self.odd_coins=self.coins[0]
						self.coins_found=True

	"""use to find the odd coins by appending the good coins holder
	  value to the list of coins
	"""

	def found_odd_coins(self):
		
		#append the good coins value to the list of available coins

		self.coins.append(self.good_coins_holder)

		#search for the odd coins, see this method for more details
		self.found_odd_coins_in_tree()		

	"""same as above method but instead of appending the good coins holder
	   to the list of coins it appending the coins holder
	"""
	def load_coins_in_hold(self):
		#appending the coins holder value to the list of coins
		self.coins.append(self.coins_holder)	
		#search for the odd coins, see this method for more details
		self.found_odd_coins_in_tree()		

		

	"""searching for the odd coins in a length of 3 coins of the coins list
	"""
	def found_odd_coins_in_tree(self):
		
		i=0
		#is coins value at index 0 equal to the coins value at index 1
		
		if (self.coins[i] == self.coins[i+1]):
			"""if the the coins value at index 0 equal to the coins
			   value at index 1 automatically the coins value at 
 			   index 2 is the odd coins and assign it to the odd
			   coins object and set the coins found object to true
			"""
			if(self.coins[i]==self.coins[i+2]):
				self.same_coins=True
	
			self.odd_coins=self.coins[i+2]

			self.coins_found=True
						 
		elif(self.coins[i] == self.coins[(i+2)]):
			"""if the coins value at index 0 equal to the coins
			   value at index 2 automatically the coins value at 
			   index 1 is the odd coins and assign it to the odd
			   coins object and set the coins found object to true
			"""
		
			self.odd_coins=self.coins[i+1]

			self.coins_found=True
							
		else:
			"""In case none of above statement are true so the odd
			   coins is at index 0 and set the coins found object
			   to true
			"""					
			self.odd_coins=self.coins[i]
			self.coins_found=True

		#print(self.coins_group_holder)	

#		self.load_existing_coins_group()	
	
	"""use to find which group of coins contain the odd coins
           Parameter1 : group of coins
	   Return     : void
	"""

	def find_group_coins(self,coins_group):


		"""check if the sum of coins group at index 0 equal to the
		   one at index 1
		"""		
		if((sum(self.coins_group[0]))==(sum(self.coins_group[1]))):
			"""If the sum of coins group at index 0 is equal to 
			   the one at index 1 means that the coins group at
			   index 2 cointains the odd coins and initialize the
                           good coins holder value to the coins group value
                           of the index 0
			"""

			self.coins=self.coins_group[2]
			self.good_coins_holder=self.coins_group[0][0]

			
		elif((sum(self.coins_group[0]))==(sum(self.coins_group[2]))):

			"""check if the sum of group at index 0 equal to the 
			   grop at index 2
			"""
			#initialize the coin group at index 1 
			self.coins=self.coins_group[1]

			#initialize the good coins holder value
			self.good_coins_holder=self.coins_group[0][0]
	
			
		else:
			#initialize the coin group at index 0
			self.coins=self.coins_group[0]

			#initialize the good coins holder value
			self.good_coins_holder=self.coins_group[2][0]

		#self.load_existing_coins_group()

		
			

	"""This method is used to weight the coin per group
	"""
	def scale_coins(self):

		#get the size of the group
		coins_group_size=len(self.coins_group)

		#increment the index of the progress bar
		self.index+=1

		#check if the size of the group greater than 1 
		if (coins_group_size > 0):

			#increment the weighting number to 1
			self.number_of_weigthing+=1
 
		
			# is the size of the group divisible by 3
			if(coins_group_size % 3.0 == 0):

				#use the find group to the group that has the
			        #the fake coins	
				self.find_group_coins(self.coins_group)

				
			#else:
			#	"""if the group is not divisible by 3 use the
			#	   below method to find the fake coins group
			#	"""
			#	self.find_right_group(self.coins_group)		
			
			self.load_existing_coins_group()

	"""use to change the 2 division group into 3 division group
	"""			

	def change_group_size(self):
		#get the size of the current coins		
		len_coins=len(self.coins)

		if(len(self.coins_group_holder) == 0):

			number_of_coins_per_group=int(len_coins/3)
		
			new_coins_length=number_of_coins_per_group * 3

			rest_of_coins=len_coins - new_coins_length

			new_coins=self.coins[0:new_coins_length]
		
			self.coins_group_holder=self.coins[new_coins_length:len_coins]
			self.divider=3
			
			self.coins=new_coins

			self.is_change_group_in_hold=True


	"""method use to find the right group that contains the fake coins
	  Paramter1 : coins group as a list
	  Return    : void
	"""		
	def find_right_group(self,coins_group):

		j=0
		#size of the coin group
		group_size=len(coins_group)

		#declare to hold the key previous explore coins
		previous_coins_holder=0

		#hold the boolean of difference between 2 coins
		is_coins_diff_find=False

	
		#loop through the coins group
		
		while (j < group_size):

	
			i=0
			#for each value in the first group do something
			for i in range(len(coins_group[j])):

				#store the current value of the first group of i index
				cur_coins_value=coins_group[j][i]
		
				#check if the current iter index is 0
				if(i==0):

					#save this value as previous one
					previous_coins_holder=cur_coins_value

				else:
					#check if the previous value different than the current one

					if(previous_coins_holder != cur_coins_value):
						#we find the fake coins
						is_coins_diff_find=True
					
						#save this group as fake coins group
						self.coins=coins_group[j]

						#check if this is the first index in the group					
						if (j==0):
							#set the good coins value to be the next group index of the first element value
							self.good_coins_holder=coins_group[j+1][0]
						else:
							#set the good coins value to be the first group index of the first element
							self.good_coins_holder=coins_group[0][0]
	
					#set the previous holder value to the current coins value
					previous_coins_holder=cur_coins_value

				#increment the index to one

				i+=1


			j+=1		
				

		 
class Rsa(e_object):

	def __init__(self,bits_size=1024):
		
		super().__init__()
		
		self.know_prime=[2,3]

		self.keys_modulo=None

		self.totient=None

		self.public_key=None
		
		self.private_key=None
		
		self.public_exponent=None

		self.private_exponent=None

		self.text_encrypted=None

		self.text_decrypted=None

		self.encrypt_message=""
		self.prime_p=None
		self.prime_q=None

		self.static_number=942543

		self.m_verbose=[]

		self.bits_size=bits_size
	
	"""Euclid's alagorithm for determining the greatest common divisor

	"""
	def inv(self,p,q):
		t1,t0 = 1,0
		def xgcd(x,y):
			s1,s0 = 0,1
			t1,t0 = 1,0
			while y:
				q = x // y
				x,y = y, x % y
				s1, s0 = s0 - q * s1,s1
				t1,t0  = t0 -q * t1,t1
			return x, s0,t0
	 
		s, t =xgcd(p,q)[0:2] 
		if t < 0:
			t+=q
		return t 

		

	"""Check if the number is composite or not

	   Return : True if the number is composite or False if not
	"""
	
	def composite_number(self,a,d,n,s):
		
		if pow(a,d,n)==1:
			return False
		for i in range(s):
			if pow(a,2**i * d,n) == n-1:
				return False
		return True

	"""Find the prime number and check if the number it is really a prime
	"""
	def get_know_prime(self):
		self.know_prime+=[x for x in range(5,1000,2) if self.is_prime(x)]


	"""Find a prime number of a given number use a bit search
	"""
	def is_prime(self,n,huge_number=16):


		if (n in self.know_prime) or (n in (0,1)):
			return True
		if any((n%p) == 0 for p in self.know_prime):
			return False
		d,s = n - 1,0
		while not (d %2):
			d,s=d >> 1,s+1
		if n < 1373653:
			return not any(self.composite_number(a,d,n,s) for a in (2,3))
				
		if n < 25326001:
			return not any(self.composite_number(a,d,n,s) for a in (2,3,5))
		
		if n < 118670087467:

			if n == 3215031751:
				return False
			return not any(self.composite_number(a,d,n,s) for a in (2,3,5,7))
		
		if n < 2152302898747:
			return not any(self.composite_number(a,d,n,s) for a in (2,3,5,7,11))
		
		if n < 3474749660383:
			return not any(self.composite_number(a,d,n,s) for a in (2,3,5,7,9,11,13))
		
		if n < 341550071728321:
			return not any(self.composite_number(a,d,n,s) for a in (2,3,5,7,11,13,17))
		
		return not any(self.composite_number(a,d,n,s) for a in self.know_prime[:huge_number])


	"""Find prime number using a bit search


	   Paramater1 : set the bit number to use to provide the prime number
	   Parameter2 : number of search it will take to find the prime number
	   Return : the prime number if found otherwise 1 for not
	"""
	def searching_prime_number(self,bits_number,count_search=50):

		is_prime_number=False

		ran_num=None

		search_index=0

		self.get_know_prime()

		while not is_prime_number:

			ran_num=random.getrandbits(bits_number) 

			is_prime_number=self.is_prime(ran_num)	
			
			if((not is_prime_number) and search_index==count_search):
				break
			search_index+=1

		if(is_prime_number):

			return ran_num
		else:
			return 1

	"""Generate the modulo n and the totient Q(n)

	   Return : void
	"""

	def generate_key_modulo_totient(self):

		#get the prime number of p using 1024 bits by default
		self.prime_p=self.searching_prime_number(self.bits_size,9999)
		#get the prime number of q using 1024 bits by default
		self.prime_q=self.searching_prime_number(self.bits_size,9999)
		
		"""Check if p equal to p and both number is 1
		"""
		if(self.prime_p==self.prime_q) or self.prime_p==1 or self.prime_q==1:
	
			#if the above statement is valid recurse this method again
			self.generate_key_modulo_totient()

		else:
			"""If the above statement is not true calcule the modulo
			   n of p and q.And also calcule the totient Q(n) of n
			"""
			self.key_modulo=self.prime_p * self.prime_q
			self.totient=(self.prime_p-1) * (self.prime_q-1)
		
	"""Get the gcd of the 2 number use interraction to make it faster
	"""	
	def get_gcd(self,num_1,num_2):

		while num_2 !=0 :
			num_1,num_2 = num_2, num_1 % num_2

		return num_1


	def get_gcd_pub_exponent(self):

		pub_exponent=random.randrange(self.static_number,self.totient)

		g=self.get_gcd(pub_exponent,self.totient)

		while g!=1:

			pub_exponent=random.randrange(self.static_number,self.totient)
			
			g=self.get_gcd(pub_exponent,self.totient)

		return pub_exponent



	"""Find the public key using the totient generate previously
	"""

	def generate_public_key(self):
		
		#getting the public exponent
		public_key=self.inv(self.static_number,self.totient)

		self.m_verbose.append("Findind the publuc key exponent")
		self.m_verbose.append("Total time use to find the public key :%s"%self.get_runtime())

		return public_key

	"""write a private key into a file called private.exp
	"""

	def f_private_key(self):
		"""open a file called private.exp or create one if not exists
		   and write the modulo n and the private key
		   using this 'with open ' statement to make sure the file
                   will properly closed
		"""
		with open("private.exp","w") as fo:
			#write the key modulo in form of hex and append the plus 			#to separate the key
			fo.write(self.int2Hex(self.key_modulo)+"+")
			#write the private key in form of hex
			fo.write(self.int2Hex(self.private_exponent))

	"""write a public key into a file called public.exp
	"""
	def f_public_key(self):		
		"""open a file called public.exp or create one if not exists
		   and write the modulo n and the public key
		   using this 'with open ' statement to make sure the file
                   will properly closed
		"""
		with open("public.exp","w") as fo:			
			#write the key modulo in form of hex and append the plus 			#to separate the key
			fo.write(self.int2Hex(self.key_modulo)+"+")
			#write the public key in form of hex
			fo.write(self.int2Hex(self.public_exponent))

	"""Called to generate the public and the private key into a file
	"""

	def f_generate_pub_priv_key(self):
		#get the public and private key
		self.generate_pub_priv_key()
		#save the public key into a file
		self.f_public_key()
		#save the private key into a file
		self.f_private_key()
	
	"""Encrypt a content of a file and save it in out.ppk file by default
	   Parameter1	: file that contains the data to encrypt
	   [Parameter2] : the output the file by default out.ppk
	   [Parameter3] : the public key component by default public.exp
	   Return 	: void
	"""
	def f_encrypt_with(self,in_file_name,out_file_name="out.ppk",public_key_file_name="public.exp"):
		
		#will hold the contains of the original file per line
		file_data=""

		key_data=[]#hold the public and module key for the encryption

		str_key_data=""#hold the 

		try:
			#read all the line from the input file
			with open(in_file_name,"r") as fi:
				for line in fi:
					file_data+=line
			#read the all the key from the public file 
			with open(public_key_file_name,"r") as fi_priv:
				str_key_data=fi_priv.read()

			
			#convert the hex to a list of of long integer
			key_data=self.hex2List(str_key_data)

			#retrive the module n from the list
			self.key_modulo=key_data[0]
			#retrieve/get the public key exponent of the list
			self.public_exponent=key_data[1]

			#encrypt the contains of the file
			self.encrypt_text(file_data)

			#write the encrypt data into a file out.ppk
			with open(out_file_name,"w") as fo:
				fo.write(self.text_encrypted)

		except Exception:
			pass

	"""Encrypt a contain of a file and by default save it into encrypt.data
	"""
	def f_encrypt(self,in_file_name,out_file_name="encrypt.data"):

		#generate the public and private key exponent
		self.generate_pub_priv_key()

		#declare to hold the contains of the original file per line
		file_data=""
		
		try :
			#read the file line per line with this statement
			with open(in_file_name,'r') as fi:
				for line in fi:
					file_data+=line

			#encrypt the contain of the file
			self.encrypt_text(file_data)
			"""save the private key into a file for the user 
			   to use later to decrypt the file back
			"""
			self.f_private_key()
			
			#write the encrypt data into the ouput file by default encrypt.data
			with open(out_file_name,"w") as fo:

				fo.write(self.text_encrypted)	
	
		except IOError as e:
			pass			
			
	"""Read the encrypt contains of the given file and start decrypt the 
	   contains
	"""	
	def f_decrypt(self,in_file_name="encrypt.data",out_file_name="decrypt.data",private_key_file_name="private.exp"):

		#hold the contain of the given encrypt file
		file_data=""

		key_data=[]#hold the private and modulo key 

		str_key_data=""#the private file name data per line

		try:
			"""Read the entire file per line
			"""
			with open(in_file_name,"r") as fi:
				for line in fi:
					file_data+=line

			"""Read all the key from the given file
			"""
			with open(private_key_file_name,"r") as fi_priv:
				str_key_data=fi_priv.read()
			
			#change the encrypt contains into a list of long integer
			key_data=self.hex2List(str_key_data)

			#get the modulo n from the list
			self.key_modulo=key_data[0]
			#get the private key exponent d from the list
			self.private_exponent=key_data[1]

			#decrypt the contains
			self.decrypt_text(file_data)

			#save the decrypt contains into the output file
			with open(out_file_name,"w") as fo:
				fo.write(self.text_decrypted)		
		

		except IOError as e:
			pass


	"""finding the private key exponent d from the public key and
	   the totient key given

	   Return	: the private key exponent
	"""
	def part_of_inv(self,public_exponent,totient):
		#check if the totient is 0
		if totient==0:return (1,0)
		"""The below code try to find the inverse of the public key
		   and return the key
		"""
		(q,r) = (public_exponent//totient,public_exponent%totient)
		(s,t) = self.part_of_inv(totient,r)
		return (t,s-(q*t))

	"""Short method to find the inverse of the public key and return the 
	   finding key
	"""
	def find_inverse(self,public_exponent,totient):
		inv=self.part_of_inv(public_exponent,totient)[0]
		if inv < 1 : inv +=totient
		return inv
		

	"""Get the private key with the public key exponent e and the totient
	   Q(n)
	"""
	def generate_private_key(self,pub_key):

		priv_key=self.find_inverse(pub_key,self.totient)

		return priv_key


	"""Convert text into integer
	   Parameter1	: text to convert
	   Return	: map of integer
	"""
	def text2Int(self,text):
		return reduce(lambda x,y : (x<<8) + y,map(ord,text))

	"""Convert integer into a text
	   Parameter1	: number to convert
	   Parameter2	: bit size to use
	   Return	: text converted
	"""
	def int2Text(self,number,size=8):
		text="".join([chr((number >> j) & 0xff) for j in reversed(range(0,size << 3,8))])
		return text.lstrip("\x00")

	"""Convert integer to a list
	   Parameter1	: given integer number
	   Parameter2	: number of bit to use
	   Return 	: a list of integer
	"""
	def int2List(self,number,size):
		return [(number >> j) & 0xff for j in reversed(range(0, size << 3,8))]

	"""Convert list into integer
	   Parameter1	: list of integer
	   Return	: integer converted
	"""
	def list2Int(self,listInt):
		return reduce(lambda x,y : ( x << 8) + y, listInt)


	"""Get the size of the modulo key n
	   Return	: size of the modulo key n
	"""
	def modSize(self):
		return len("{:02x}".format(self.key_modulo)) // 2

	"""Generate public and private key exponent
	   Return : tuple of public and private key
	"""
	def generate_pub_priv_key(self):
		"""generate the modulo n and the totient Q(n)
		"""
		self.generate_key_modulo_totient()
		"""Get the public key exponent e such that gcd(e,Q(n)) equal 1
		"""
		self.public_exponent=self.generate_public_key()

		"""Get the private key exponent d such that de=1 + (K * Q(n))
		"""
		self.private_exponent=self.generate_private_key(self.public_exponent)

		#create a public key
		self.public_key=(self.key_modulo,self.public_exponent)

		#create private key
		self.private_key=(self.key_modulo,self.private_exponent)
		
		#return a tuple of the public and private key
		return ((self.key_modulo,self.public_exponent),(self.key_modulo,self.private_exponent))


	
	"""return the public key exponent
	   Return :hex decimal value
	"""
	def get_public_key_exponent_hex(self):
		return self.int2Hex(self.public_exponent)

	"""return the private key exponent
	   Return : hex decimal value
	"""
	def get_private_key_exponent_hex(self):
		return self.int2Hex(self.private_exponent)


	
	"""return the public key exponent
	   Return :integer value
	"""
	def get_public_key_exponent_int(self):
		return self.public_exponent

	"""return the private key exponent
	   Return : integer value
	"""
	def get_private_key_exponent_int(self):
		return self.private_exponent

	"""Ecnrypt any text given 
	   Parameter1	: plain text to encrypt
	   Return	: cipher text
	"""
	def encrypt_text(self,plaintext):
		encrypt_text=[]#list of cipher text
		encryp_ms=""

		#in each caracter found in the given plain text 
		for char in plaintext:

			#convert the char into integer and change the bit size
			convert_char=ord(char)<<16

			
			"""With the integer value get from the above conversion
			   make sure the encrypt message is m_enc=(convert_char 		           ^ e )
			"""
			long_int=pow(convert_char,self.public_exponent,self.key_modulo)
			#set each integer calculation into the encrypt text list

			encrypt_text.append(pow(convert_char,self.public_exponent,self.key_modulo))
		
		#convert the encrypt text list into an hex file	
		self.text_encrypted=self.List2Hex(encrypt_text)
		#return the list of the encrypt integer
		return encrypt_text

	"""return the cipher text recently encrypted
	   Return : String object represent the cipher text
	"""

	def get_cipher_text(self):
		return self.text_encrypted


	
	"""return the decrypt text recently encrypted
	   Return : String object represent the plain text
	"""
	def get_decrypt_text(self):
		return self.text_decrypted

	"""Convert a given number into a string
	   Parameter1	: given number to convert
	   Return	: a join string data
	"""
	def number_to_string(self,number,n=3):
		num_str = str(number)
		if len(num_str) < n:
			num_str='0'*(n-len(num_str)) + num_str
		elif len(num_str) %n !=0:
			num_str='0'*(n-len(num_str)%n)+num_str
		print(num_str)
		chars = re.findall('.'*n,num_str)
		l=[chr(int(i)) for i in chars]
		return ''.join(l)

	"""Decryt a given cipher text
	   Parameter1	: cipher text to decrypt
	   Return	: decrypt text     
	"""
	def decrypt_text(self,cipher_text):		
		#convert hex text into a list of integer
		cipher_int=self.hex2List(cipher_text)
		#convert a list into integer
		list2int=self.list2Int(cipher_int)
		#set the text encrypted
		self.text_decrypted=""
		#initialize an object to hold the current state of the result
		error_detected=False
		#initialize an object to hold the error message 
		error_message=""

		#loop througth the cipher text
		for char_int in cipher_int:
			try:
				"""with each interaction we have to make sure
				   our response is mdecry=(char_in ^ d mod n)
				"""
				bytes2int=pow(char_int,self.private_exponent,self.key_modulo)
				"""once retrieve the caracter divide back the
				   integer in 2^n where n=16 
				"""
				real_int=bytes2int>>16

				"""Convert the find integer to ascii caracter
				   and save it append it to the decrypt text obj
				"""
				self.text_decrypted+=chr(real_int)
			except OverflowError as ex:
				error_detected=True
				error_message=ex
				break
		#in case there is any error print to the screen
		if error_detected:

			print("There is an error decrypting the message")

		else:
			#if no error find return the decrypt text
			return self.text_decrypted

	"""Convert integer to hex number
	   Parameter1	: number to conver
	   Return	: the exact base number that macthes that integer value
	"""
	def int2Hex(self,number):
		return ("{:02x}".format(number)).upper()
	
	"""Convert an hex base number into an integer
	   Parameter1	: hex base number given
	   Return	: an integer represent the hax number in n bit where 
				n=16
	"""
	def hex2Int(self,hex_str):
		return int(hex_str,16)

	
	"""Convert a list of integer into hex number
	   Paramter1	: given list of interger
	   Return	: string of hex number
	"""
	def List2Hex(self,intList):

		list2hex=""

		for index,elem in enumerate(intList):
			if index % 32 == 0:
				pass
			int2Hex=("{:02x}".format(elem)).upper()
			str_len=len(int2Hex)
			list2hex+=int2Hex.ljust(str_len+1,"+")
		
		return list2hex


	"""Convert a string of hex number base into a list of integer
	   Parameter1	: given a string represent the hex value
	   Return	: list of integer
	"""
	def hex2List(self,hexstr):

		cleanString=re.sub("\++",",",hexstr)

		hex2List=cleanString.split(",")

		listInt=[]

		for index,elem in enumerate(hex2List):
			if elem !="":
				#print("hex in list=>%s"%elem)

				hex2Int=int(elem,16)

				listInt.append(hex2Int)
		return listInt
		
	"""Display integer value
	   Parameter1	: given number 
	   Return	: void
	"""
	def printLargeInteger(self,number):
		string="{:02x}".format(number)
		for j in range(len(string)):
			if j % 64 == 0:
				print()
			print(string[j],end="")
		print()
