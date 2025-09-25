while True:
    try:
        x=int(input("Pick a number."))
        break
    except ValueError:
        print("Nope.")
if x%5==3:
    print("Congratulations! You win a free hug.")
else:
    print("This was just a waste of your time.")
