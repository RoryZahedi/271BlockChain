import hashlib


options = {'1':'transfer', '2': 'balance check'}

class BlockChain:
    def __init__(self):
        self.head = None
        self.size = 0
    def printBlockChain(self):

        print('\n\n')
        n = self.head
        count = 0
        line0 = "           "
        line1 = "Sender(PID) | " #sender
        line2 = "Receiver    | " #receiver
        line3 = "Amount      | " #amount
        line4 = "Status      |" #status
        line5 = "Prev:"
        line7 = "CLK         | " 
        while(n):
            line0 += "T" + str(count) + "     "
            count += 1
            line1 += n.transaction.sender + "     "
            line2 += n.transaction.receiver + " --> "
            line3 += n.transaction.amount + "     "
            line4 += " " + str(n.status) + "    "
            line5 += n.prev + ","
            line7 += str(n.transaction.CLK) + "     "
            n = n.next
        print(line0)
        bar = "-"*len(line1)
        print(bar)
        print(line1)
        print(line2)
        print(line3)
        print(line4)
        print(line7)
        print('\n\n')
        print(line5)



    def insertTransaction(self,transaction): 
        newBlock = Block(transaction)
        if self.head == None: #Empty blockchain
            self.head = newBlock
            newBlock.prev = ""
        else: 
            n = self.head
            prev = None
            # self.printBlockChain()
            while(n): #iterate til we find head of requests
                if n.status == 0:
                    break
                else:
                    prev = n
                    n = n.next      
            while n: #find where to insert based off clock and use PID (sender) to break ties
                if int(n.transaction.CLK) > int(newBlock.transaction.CLK): #if new block's clock preceeds current block 
                    break
                if int(n.transaction.CLK) == int(newBlock.transaction.CLK): #tie on clock, break tie with PIDs
                    if int(n.transaction.sender) > int(newBlock.transaction.sender):
                        break
                prev = n
                n = n.next
            if not prev: #Inserting at head of list
                temp = self.head
                self.head = newBlock
                self.head.next = temp
            else:
                prev.next = newBlock
                newBlock.next = n
            #Recompute hashes of new block and everything down til end of the list
            n = newBlock
            while(n):
                if n != self.head: #head has no has
                    hasher = hashlib.sha256()
                    hasher.update((prev.transaction.sender +  prev.transaction.receiver +  str(prev.transaction.amount) + prev.prev + str(prev.transaction.CLK)).encode())
                    n.prev = hasher.hexdigest()
                prev = n
                n = n.next

    def setStatus(self,statusNum): #sets status as statusNum for head of requests, and determines new head of requests
        headOfRequests = self.getHeadOfRequests()
        headOfRequests.status = statusNum
    def getHeadOfRequests(self):
        n = self.head
        while(n): #iterate til we find head of requests
            if n.status == 0:
                break
            else:
                prev = n
                n = n.next     
        return n #n could be none!





        


class Block: #Each block contains only one transaction
    def __init__(self, transaction):
        self.transaction = transaction
        self.next = None
        self.status = 0 #Pending = 0, Committed = 1, Aborted = -1
        self.prev = " "
    def __repr__(self):
        return self.transaction

class Client:
    def __init__(self):
        self.ClientBlockChain = BlockChain()
        self.balance = 10
        #Lamport totally ordered clock

class Transaction:
    def __init__(self,sender,receiver,amount,CLK):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.CLK = CLK
    

            

    