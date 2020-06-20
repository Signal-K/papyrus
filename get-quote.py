import random # imports the "random" python module that allows us to choose random numbers
def primary():
  # print("Keep it logically awesome.")

  f = open("quotes.txt")
  quotes = f.readlines()
  f.close()

  # print(quotes[0])
  last = 13 # We have 14 (index values) quotes in quotes.txt, so the possible random values (see below line) are 0-13, or the 1st quote to the 14th
  rnd = random.randint(0, last) 
  print(quotes[rnd])

  if __name__== "__primary__":
    primary()
