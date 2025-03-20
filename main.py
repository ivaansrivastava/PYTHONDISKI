# COPYRIGHT By IVAAN (github.com/leaperstuff)
# MIT License
# FREE TO USE

#import libs
import subprocess

# Main menu

print("Choose:")
print("1. Notes")
print("2. Exit")
choice = input("Enter choice: ")

# Choices
if choice == "1":
	subprocess.run(["python", "notes.py"])
elif choice == "2":
	print("Exiting...")
	exit()
else:
	print("Invalid choice")
	# New lesson: Indents matter in python