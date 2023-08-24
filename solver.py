from itertools import combinations
import math
import json


def combination_(initial_list:list) -> list:
    indexes=[]
    result=[initial_list]
    for i in range(len(initial_list)):
        if initial_list[i]==0:
            indexes.append(i)
    n=len(indexes)
    for i in range(1,n+1):
        combs=combinations(indexes,i)
        for comb in combs:
            tmp=initial_list.copy()
            for index in comb:
                tmp[index]=1
            result.append(tmp)
    return result


def try_all_combinations(combs:list, char:chr, list_of_words: list ) -> dict:
    result={}
    for word in list_of_words:
        for i,comb in enumerate(combs):
            is_matching=True
            for k in range(len(comb)):
                if(comb[k]==1 and word[k]!=char):
                    is_matching=False
                    break
                if(comb[k]!=1 and word[k]==char):
                    is_matching = False
                    break
            if(is_matching):
                if i not in result:
                    result[i]=[]
                result[i].append(word)
                break

    return result


def calculate_entropy(n:int, dic:dict)->float:
    s=0
    for key in dic:
        p=len(dic[key])/n
        s+=-p*math.log2(p)
    return s


def best_guess(guesses : list, words : list, current_state : list) -> (chr, list, dict):
    result=""
    possible_state={}
    max=0
    n=len(words)
    combs=combination_(current_state)
    for guess in guesses:
        dic=try_all_combinations(combs, guess, words)
        s=calculate_entropy(n,dic)
        if s>max:
            max=s
            result=guess
            possible_state=dic

    return result,combs, possible_state


def output_format(current_state:list) -> str:
    output=""
    for k in current_state:
        if(k==0):
            output+='_'
        else:
            output+=k

    return output


def input_format(input:str) -> list:
    result=[]
    for l in input:
        if l=='_':
            result.append(0)
        else:
            result.append(l)

    return result


def find_index(look : list,combs  : list ) -> int :
    for i,comb in enumerate(combs):
        is_matching=True
        for k in range(len(comb)):
            if look[k]!=comb[k]:
                is_matching=False
                break
        if(is_matching):
            return i

    return -1


def find_comb(old_state : list, new_state : list)->list:
    result=[]
    for i in range(len(old_state)):
        if old_state[i]!=new_state[i]:
            result.append(1)
        else:
            result.append(old_state[i])
    return result


def check_input(inp : str, guess : chr, current_state : list) -> bool:
    if len(inp) != len(current_state) :
        return False

    for i in range(len(inp)):
        if current_state[i] == 0:
            if inp[i] != '_' and inp[i] != guess:
                return False
        else:
            if inp[i] != current_state[i]:
                return False
    return True


def get_data(file_name : str) -> dict :
    with open(file_name) as json_file:
        data = json.load(json_file)
    data = {int(key): value for key, value in data.items()}
    return data




