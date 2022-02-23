import os
os.chdir("G:/My Drive/EverythingElseBackup/Python_fun_projects/Wordle_solver")
import pandas as pd
import numpy as np
import scipy as sp
import csv
from numpy import loadtxt
from collections import Counter
from itertools import compress
import pandas as pd


pl = open('possible.txt', 'r').read().replace("'", "").split(",") # the 2000 words to solve
possible = sorted(pl)
ml = open('master.txt', 'r').read().replace("'", "").split(",")
master = sorted(ml+possible)

al = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


#Frequency model
plc = sorted(Counter(''.join(possible)), key=Counter(''.join(possible)).get, reverse=True)
mlc = sorted(Counter(''.join(master)), key=Counter(''.join(master)).get, reverse=True) #totals
mlcw = [i / sum(Counter(''.join(master)).values()) for i in list(Counter(''.join(master)).values())] #weights 


#sort by single letter frequency
letter_sorted_master = []
#sort master list by letter frequency in Master
for alpha in range(0,26):
    for i in range(0, len(master)):
        if mlc[alpha] in master[i]:
            letter_sorted_master.append(master[i])

letter_sorted_master = [i for n, i in enumerate(letter_sorted_master) if i not in letter_sorted_master[:n]]
len(letter_sorted_master)
################## spanning the uncertainty space

rrun = 10000
#rrun = 10
solution_counter = []
word_list = []
guess_words = []
first_mword = []
# second_mword = []
# third_mword = []
# fourth_mword = []
# fifth_mword = []
# sixth_mword = []
word_saver = np.zeros((rrun, 50), dtype = object)
#alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for xxx in range(0,rrun):
    word = possible[np.random.randint(0,len(possible))]
    mword = letter_sorted_master[np.random.randint(0,len(letter_sorted_master))]
    #word = possible[np.random.randint(0,10)]
    #mword = letter_sorted_master[xxx]    
    #mword = letter_sorted_master[xxx]
    #word = 'chase'
    #mword = 'stare'
    # first_mword.append(mword)    
    word_list.append(word)
    filtered_master = letter_sorted_master

    for ooo in range(0,30): 

        word_saver[xxx,ooo] = mword
        if word == mword:
            solution_counter.append(ooo+1)
            guess_words.append(mword)
            print(xxx)
            break


        #removing the words with letters are incorrect positions
        eperm_index = []
        for i in range(0,5):
            if mword[i] != word[i]:
                eperm_index.append(i)

        if len(eperm_index) >0:
            esuper_master = []
            esuper_master.append(filtered_master)
            esuper_master.append(list(set(esuper_master[0]) - set((list(compress(esuper_master[0], np.char.find(esuper_master[0], mword[eperm_index[0]]) == eperm_index[0]))))))
        if len(eperm_index) > 1:
            esuper_master.append(list(set(esuper_master[1]) - set((list(compress(esuper_master[1], np.char.find(esuper_master[1], mword[eperm_index[1]]) == eperm_index[1]))))))
        if len(eperm_index) > 2:
            esuper_master.append(list(set(esuper_master[2]) - set((list(compress(esuper_master[2], np.char.find(esuper_master[2], mword[eperm_index[2]]) == eperm_index[2]))))))
        if len(eperm_index) > 3:
            esuper_master.append(list(set(esuper_master[3]) - set((list(compress(esuper_master[3], np.char.find(esuper_master[3], mword[eperm_index[3]]) == eperm_index[3]))))))
        if len(eperm_index) > 4:
            esuper_master.append(list(set(esuper_master[4]) - set((list(compress(esuper_master[4], np.char.find(esuper_master[4], mword[eperm_index[4]]) == eperm_index[4]))))))

        perm_index = []
        for i in range(0,5):
            if mword[i] == word[i]:
                perm_index.append(i)

        #get set of words with letters at exact position, if any
        super_master = []
        if len(perm_index) == 0:
            super_master.append(esuper_master[len(eperm_index)])
        if len(perm_index) > 0:
            super_master.append((list(compress(esuper_master[len(eperm_index)], np.char.find(esuper_master[len(eperm_index)], mword[perm_index[0]], start=perm_index[0]) ==perm_index[0]))))
        if len(perm_index) > 1:
            super_master.append((list(compress(super_master[0], np.char.find(super_master[0], mword[perm_index[1]], start=perm_index[1]) ==perm_index[1]))))
        if len(perm_index) > 2:
            super_master.append((list(compress(super_master[1], np.char.find(super_master[1], mword[perm_index[2]], start=perm_index[2]) ==perm_index[2]))))
        if len(perm_index) > 3:
            super_master.append((list(compress(super_master[2], np.char.find(super_master[2], mword[perm_index[3]], start=perm_index[3]) ==perm_index[3]))))
        if len(perm_index) > 4:
            super_master.append((list(compress(super_master[3], np.char.find(super_master[3], mword[perm_index[4]], start=perm_index[4]) ==perm_index[4]))))


        aperm_index = []
        eli_index = []
        for i in range(0,5):
            if mword[i] in word:
                aperm_index.append(i)
            if mword[i] not in word:
                eli_index.append(i)


        #removal of letter/s that dont appear in the word
        if len(eli_index) == 0:
            super_master == super_master
        if len(eli_index) > 0:     
            super_master[len(perm_index)-1] = list(set(super_master[len(perm_index)-1]) - set((list(compress(super_master[len(perm_index)-1], np.char.find(super_master[len(perm_index)-1], mword[eli_index[0]]) >= 0)))))
        if len(eli_index) > 1:     
            super_master[len(perm_index)-1] = list(set(super_master[len(perm_index)-1]) - set((list(compress(super_master[len(perm_index)-1], np.char.find(super_master[len(perm_index)-1], mword[eli_index[1]]) >= 0)))))
        if len(eli_index) > 2:     
            super_master[len(perm_index)-1] = list(set(super_master[len(perm_index)-1]) - set((list(compress(super_master[len(perm_index)-1], np.char.find(super_master[len(perm_index)-1], mword[eli_index[2]]) >= 0)))))
        if len(eli_index) > 3:     
            super_master[len(perm_index)-1] = list(set(super_master[len(perm_index)-1]) - set((list(compress(super_master[len(perm_index)-1], np.char.find(super_master[len(perm_index)-1], mword[eli_index[3]]) >= 0)))))
        if len(eli_index) > 4:     
            super_master[len(perm_index)-1] = list(set(super_master[len(perm_index)-1]) - set((list(compress(super_master[len(perm_index)-1], np.char.find(super_master[len(perm_index)-1], mword[eli_index[4]]) >= 0)))))

        
        net_index = [x for x in aperm_index if x not in perm_index]

        #keeping the set only with the letters that appear somewhere in the word
        afiltered_master = []
        if len(net_index) == 0:
            afiltered_master = [super_master[len(perm_index)-1]]
        if len(net_index) > 0:
            afiltered_master.append(list(compress(super_master[len(perm_index)-1], np.char.find(super_master[len(perm_index)-1], mword[net_index[0]]) >=0)))
        if len(net_index) > 1:
            afiltered_master.append(list(compress(afiltered_master[0], np.char.find(afiltered_master[0], mword[net_index[1]]) >=0)))
        if len(net_index) > 2:
            afiltered_master.append(list(compress(afiltered_master[1], np.char.find(afiltered_master[1], mword[net_index[2]]) >=0)))
        if len(net_index) > 3:
            afiltered_master.append(list(compress(afiltered_master[2], np.char.find(afiltered_master[2], mword[net_index[3]]) >=0)))
        if len(net_index) > 4:
            afiltered_master.append(list(compress(afiltered_master[3], np.char.find(afiltered_master[3], mword[net_index[4]]) >=0)))
        

        if len(afiltered_master) > 1:
            filtered_master = afiltered_master[len(net_index)-1]
        if len(afiltered_master) == 1:
            filtered_master = afiltered_master[0]

        if len([filtered_master][0]) == 1:
            mword = filtered_master[0]
        if len([filtered_master][0]) > 1:
            mword = filtered_master[np.random.randint(0,len(filtered_master))]

        if word == mword:
            word_saver[xxx,ooo+1] = mword
            solution_counter.append(ooo+2)
            guess_words.append(mword)
            print(xxx)
            break
        filtered_master.remove(mword)


np.mean(solution_counter)

#writer = pd.ExcelWriter('solutioncounter_skill.xlsx', engine='xlsxwriter')
wrd = pd.DataFrame(word_saver).replace(0, '')
#pd.concat([pd.DataFrame([solution_counter,word_list, guess_words]).T,wrd],axis=1).to_excel(writer, sheet_name = 'Counter', header = ['Tries', 'OrigWord', 'GuessedWord', 'First', 'Sec', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third'])
pd.concat([pd.DataFrame([solution_counter,word_list, guess_words]).T,wrd],axis=1).to_csv('testing.csv', header = ['Tries', 'OrigWord', 'GuessedWord', 'First', 'Sec', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third', 'Third'])

#writer.save()

len(solution_counter)
word_list
guess_words
len(guess_words)



# pd.DataFrame(solution_counter).to_excel(writer,sheet_name = 'counter')
# pd.DataFrame(word_list).to_excel(writer, sheet_name = 'Orig list')
# pd.DataFrame(guess_words).to_excel(writer, sheet_name = 'Guessed list')
# pd.DataFrame(first_mword).to_excel(writer, sheet_name = 'First mword')
#pd.DataFrame(second_mword).to_excel(writer, sheet_name = 'Second mword')





