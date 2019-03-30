from Assignment import MissionaryCarnibal,Coins,Rsa

#Misionaries and carnibals problem

"""To solve this problem I use 2 kinds of algorithm ,either by brute force or
    by breadth first

To call those methods and to see how it works:
in missionary_carnibal function below write
all your statements and encomment this function in the main function
Create the missionary and carnibal object with MissionaryCarnibal class
his class has 2 arguments:the first argument represent the number of 
missionaries and the second one is the number of carnibals
once the object was declare initiate the number of object that

MissionaryCarnibal	: class to be call to initiate the number of 
				missionaries and carnibals as parameters

boat_capacity		: object method that represent the numbers of objects
				that the boat can carry	

move_carnibal_and_missionary	:object method that represent the brute force 
				  algorithm to move all the objects
run_time		: parent object method to check the execution time in
				seconds
bread_search		: object method that run the breadth first algorithm 
			    this method has one optional parameter which by 
			    default is set to false but you can set to true
                            to view other possibility to reach the goal state

"""
def missionary_carnibal():
	#initialize the object carnibal and missionary
	missionary_carnibal=MissionaryCarnibal(3,3)

	#initialize the number of object to carry
	missionary_carnibal.boat_capacity=2

	"""The below method can be called to see the brute force algorithm
	   but a i have comment it to show only the breadth first one 
	"""
	#missionary_carnibal.move_carnibal_and_missionary()

	"""The below method once called will start moving all the object to 
	   the goal state
	"""
	missionary_carnibal.bread_search()

	"""Called to view how long it take the algorithm to find/complete
	   his task
	"""
	missionary_carnibal.run_time()


#Coins problem
"""

Coins		: class to be initialize to find solution for the coins problem

finding_coins	: object method to be use to search the solution for the coins
		  problem.You have 2 ways to initialize all the coins,one way
		  is to set the coins as a list and give that list as a parameter
		  to this method and in other way is to called the init_coins 
	          method(see below description for more details).In case you initialize
		  the init_coins method you can call this method with no 
		  parameter.

init_coins	: This method is fast and will save you a lot of time in case
                  you want to find an old coins between a list of 10 to 5000000 or more.
		  To use this method 
		  Parameter1 : the value represent the odd coins to find
		  Parameter2 : the  value represent the rest of the coins
		  Parameter3 : total size/length of all coins can be 1000-50000			 
		  Parameter4 : The index where you want to put the odd coins.
				For example in the list of 50 coins you can
				set the odd coins to be in position 27 or 21 or
				3 or so on

coins_found	: object method to check if the odd coin is found or not

verbose		: object method to display all can of warning/error message


 
"""

def coins():
	#initialize the coins object
	coins=Coins()

	#see the above description
	coins.init_coins(550,500,100000000,2000000)

	#initialize the coins for searching
	#list_coins=[10,23,21,5,2,1,45,87]

	#called to start the search
	coins.finding_coins()

	#check if the coins has been found
	if(coins.coins_found):
		#show all the warning/error message
		coins.verbose()

	#display the total number of seconds take to find the odd coins
	coins.run_time()


#RSA algorithm

"""

Rsa	: class to initialize to start the encryption
	  [Parameter1] : number of bits to use to generate the key ,the default
			 is 1024

generate_pub_priv_key : Object method to call calculate the modulo n , totient
			Q(n) , the public key exponent e and the private key
			exponent d.

get_public_key_exponent_hex	: object method to return the public key 
				  exponent e in hexadecimal form.

get_private_key_exponent_hex : object method to return the private key 
				exponent d in hexadecimal form.

get_public_key_exponent_int	: object method to return the public key 
				  exponent e in integer form.

get_private_key_exponent_int    : object method to return the private key 
				exponent d in integer form.

encrypt_text		        : object method to encrypt a plain text.This 
				  method return by default the list of integer
				  as the cipher text
			         
				  Parameter1 : plain text to encrypt

get_cipher_text			: object method represent the cipher text
 
get_decrypt_text		: object method represent the decrypt text

f_encrypt		        : object method to encrypt file

				  Parameter1 : file name to encrypt in string
				  [Parameter2] :output cipher file , this 
						parameter is optional , if not
						set the cipher text will be 
						save into a file called 
						encrypt.data

f_decrypt			:object method to decrypt  the cipher text file
				 [Parameter1]: cipher file name to decryt.This
					       paramter is optional,if not set
                                               this method will look at a file
						called encrypt.data by default

				 [Parameter2]: file represent the decrypt file.
						This parameter is also optional
						and if not set the decrypt text
						will be save into decrypt.data

				  [Parameter2]: file represent the private key
						to use to decrypt the file.This
						parameter is optional and if
						not set this method will
						look at the file called 
						private.exp

f_generate_pub_priv_key	: object method that will be use to generate both
			   the public and private exponent repectively
                            public.exp and private.exp

f_encrypt_with		:object method to be use to encrypt a plain text file.
                         this method is similar to f_encrypt but it just use
                         to encrypt a plain text file with a public exponent 
			 file
                           Parameter1 : file contains the plain text
			   [Parameter2]: cipher text file represent the output
                                         of the encrypt file.This parameter is
                                         optional and by default is out.ppk
			   [Parameter3]: public exponent file holding the 
                                         public key .This is optional and by 
					 default is public.exp
					  
                                            				 

"""
def rsa():
 
	#is_prime=False

	rsa=Rsa(2048)

	rsa.generate_pub_priv_key()

	plaintext="Hello there , how are you?.Is there anything i can help with ?"

	#rsa.encrypt_text(plaintext)

	print("Cipher text is :")

	print(rsa.get_cipher_text())

	#rsa.decrypt_text(rsa.get_cipher_text())

	print("Message decrypt : %s"%rsa.get_decrypt_text())

	#rsa.f_encrypt("file_data.txt")	

	#rsa.f_decrypt()

	#rsa.f_generate_pub_priv_key()

	#rsa.f_encrypt_with("file_data.txt","real_encry_1","public.exp")

	#rsa.f_decrypt("real_encry_1","real_decry_1.txt")

	rsa.run_time()


def main():

#	missionary_carnibal()	
	coins()
#	rsa()	



if __name__ == "__main__":
	main()
