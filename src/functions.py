import requests 


def get_names():
    """
    This function obtains all the students names from github and removes the TA´s names 
    in order to prevent confusion.
    """
    url = "https://api.github.com/repos/ironhack-datalabs/datamad0820/forks"
    respon = requests.get(url)
    names = respon.json()
    lista = set([names[i]["owner"]["login"] for i in range(29)])
    new_list = []
    for e in lista:
        if e not in ('agalvezcorell', "ferrero-felipe"):
            new_list.append(e)
    lista = new_list
    return lista

def getcoment(x,apiKey=os.getenv("TOKEN")):
    """
    This function obtains the comments in json format from every issue in datamad0820.
    """
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    coment = requests.get(f'https://api.github.com/repos/ironhack-datalabs/datamad0820/issues/{x}/comments',headers=headers)
    coments = coment.json()
    return coments

def segundo(comment):
    """
    This function obtains the second user in case it exists.
    """
    try:
        return re.findall('@\w*-?\w+',comment[0]['body'])
    except:
        return None
def grade(comment):
    """
    This function obtains the grade assigned to each pull request.
    """
    try:
        z= re.findall(r'grade:.*-',comment[0]['body'])
        z = str(z).split(':')
        z = z[1].split("-")
        return z[0]
    except:
        return None

def instructor(comment):
    """
    This function obtains the name of the instructor assigned to each PR.
    """
    try:
        return comment[0]['user']['login']
    except:
        return None

def meme(comment):
    """
    This function obtains the meme URL of each comment from the instructor.
    """
    try:
        try:
            z = re.findall(r'https:.*jpg|.*png|.*jpeg',comment[0]['body'])
            z = str(z).split('(')
            z = z[1].split("'")
            return z[0]
        except: 
            z = re.findall(r'https:.*jpg|.*png|.*jpeg',comment[0]['body'])
            z = str(z).split('(')
            return z[0]
    except:
        return None  


def getpull(x,apiKey=os.getenv("TOKEN")):
    """
    This function obtains the full lab analysis from the previous defined functions.
    """
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    res = requests.get(f"https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls/{x}", headers=headers)
    status = res.status_code
    data = res.json()  
    coments = getcoment(x)
    print(x)
    try:
        return {
            "Id":data['number'],
            "Lab":data['head']['ref'],
            "State":data['state'],
            "User":data['user']['login'],
            "User2" : segundo(coments),
            "Creado" : data['created_at'], 
            "Cerrada" : data['closed_at'], 
            "Instructor": instructor(coments),
            "Meme":meme(coments), 
            "Nota":grade(coments)}
    except:
        return {"ERROR":None}

def getlab(x,apiKey=os.getenv("TOKEN")):
    """
    This function obtains the names assigned to each lab
    Input: Pull number
    Ouput: Lab name for specifed pull
    """
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    res = requests.get(f"https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls/{x}", headers=headers)
    status = res.status_code
    data = res.json()  
    coments = getcoment(x)
    print(x)
    try:
        return {
            "Lab":data['head']['ref'],
            }
    except:
        return {"ERROR":None}