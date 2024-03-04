from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

import os
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI()


CHOPPING_BLOCK = os.environ.get('CHOPPING_BLOCK')



intro = '''In this realm where choices brightly gleam,
Pray, choose a number from one to six, it seems.
With options laid, let your selection appear,
Tell me now, which number draws you near?'''


outro = '''Alas, dear friend, thy choice did stray,
For the number thou hast picked did not find its way.
'Tis not within the bounds I did proclaim,
So let us try again, and set our aim.'''


question = '''Ah, fair patron of this humble abode,
Allow me to bestow my aid, my ode.
In tongues of yore, in verse, I'll share my light,
And guide thee through the darkest of the night.

With words as sweet as honey from the comb,
I'll weave a tapestry to guide thee home.
Be it advice or wisdom you do seek,
My quill shall scribe, my voice shall softly speak.

So tell me, gentle soul, what doth thee crave?
How canst I lend my hand to thee today?
For in this realm of knowledge vast and grand,
I stand at thy service, at thy command.'''



lack_of_travels = '''Oh, noble traveler, thy journey just begun,
No past lives, alas, under the sun.
Fear not, for 'tis a canvas yet to paint,
With each new step, a destiny to acquaint.'''

farewell = '''As twilight falls and shadows dance,
I bid thee farewell, in this fleeting trance.
May stars above guide thy path with grace,
And fortune smile upon thee in every place.

Farewell, dear friend, until we meet once more,
In this digital realm or on a distant shore.
May joy and peace attend thy way,
As thou journey forth, come what may.'''















class Bard():

  def __init__(self, name = 'Bill', role = 'shakespearean poet', task = 'In a poem, explain object-oriented programming.', question = question, intro = intro, outro = outro, farewell = farewell):
    self._name = name
    self._role = role
    self._task = task
    self._question = question
    self._intro = intro
    self._outro = outro
    self._farewell = farewell
    self._past_responses = []
    self._past_lives = {role : [question, intro, outro, farewell]}


#### Making all our getters & setter
  @property
  def name(self):
    return self._name
  @name.setter
  def name(self, name):
    self._name = name
  
  @property
  def role(self):
    return self._role 
  @role.setter
  def role(self, role):
    self._role = role
  
  @property
  def task(self):
    return self._task 
  @task.setter
  def task(self,task):
    self._task = task
  
  @property
  def question(self):
    return self._question
  @question.setter
  def question(self, question):
    self._question = question
  
  @property
  def intro(self):
    return self._intro
  @intro.setter
  def intro(self, intro):
    self._intro = intro
  
  @property
  def outro(self):
    return self._outro
  @outro.setter
  def outro(self,outro):
    self._outro = outro

  @property
  def farewell(self):
    return self._farewell
  @farewell.setter
  def farewell(self,farewell):
    self._farewell = farewell
  
  
  @property
  def past_responses(self):
    return self._past_responses
  @past_responses.setter
  def past_responses(self, past_responses):
    self._past_responses = past_responses
  
  @property
  def past_lives(self):
    return self._past_lives
  @past_lives.setter
  def past_lives(self, past_lives):
    self._past_lives = past_lives





## Function that takes accepts the AI's response and returns only the answer to the user's query.
#### Really, the API response just comes in a mess of JSON, so we just strip is away to get to the good stuff  
  def translate_response(self,response):
    answer = response.choices[0].message.content
    ## We also save our AI's answers. For later maybe?
    self.save_answers(response)
    print(answer)



## Function that saves the past response into a list
## Might use this for a later feature to go through past responses.... 
#### Might just scrap it, too.... Who knows?        
  def save_answers(self,response):
    self.past_responses.append(response)




## Function that keeps the current role of the AI, and asks for another query.
#### Want to ask our current character another question? Go ahead!
  def ask_a_question(self):
    new_task = input(f'''================================\n{self.question}\n================================\n>>>>''')
    self.task = new_task
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a {self.role}."},
        {"role": "user", "content": self.task}
      ]
    )
    self.translate_response(completion)
    


#### Bill's intro to OOP!!!
#### He changes his poem a bit each time, because I'm not checking it against a past response.
#### I thought about it for the sake of saving API tokens, but the new poems are pretty fun
  def ask_Shakepeare(self):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a Shakespearean Poet"},
        {"role": "user", "content": 'In a poem, explain object-oriented programming.'}
      ]
    )
    ## I do save his responses here, if we want to see any of them again.
    self.translate_response(response)





### Asks the user to change the AI's character. 
### Tired of Bill? Go ahead and make a new character.
### You can type anything here really, but it makes more sense to type in a person/occupation/animal(?). I can't really prevent users from typing in nonsense....       
  def make_a_role(self):
    role = input('''================================\nWho am I?\n================================\n>>>>>''').lower()
    print(f'''================================\nOk! {role.capitalize()}? You got it!''')

    ## Here we make a check to see if the role once existed.
    ## If so, save us some API tokens and use their old question
    if role in self._past_lives.keys():
      self.question = self.past_lives[role][0]
      self.intro = self.past_lives[role][1]
      self.outro = self.past_lives[role][2]
      self.farewell = self.past_lives[role][3]
    else:
      self.role = role
      ### Calling these so we can save our current new character for later, maybe...
      self.new_question()
      self.new_intro()
      self.new_outro()
      self.new_farewell()
      self.saved_past_roles()



### Continuation from above. If we made a new character, we should be getting a new question, right? This is where that happens.
  def new_question(self):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a {self.role}"},
        {"role": "user", "content": f"In the voice of a {self.role}, and ask me how you can help me."}
      ]
    )
    question = response.choices[0].message.content
    self.question = question
    self.past_responses.append(question) 



### Now that we have a new character, we'd also want a new outro, right?
  def new_outro(self):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a {self.role}"},
        {"role": "user", "content": f"In the voice of a {self.role}, and tell the number I have selected is not valid."}
      ]
    )
    outro = response.choices[0].message.content
    self.outro = outro
    self.past_responses.append(outro)



### Almost forget to make and save a new intro... Sleepy...
  def new_intro(self):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a {self.role}"},
        {"role": "user", "content": f"In the voice of a {self.role}, ask me to select a number between 1 and 6."}
      ]
    )
    intro = response.choices[0].message.content
    self.intro = intro
    self.past_responses.append(intro)


### Adding a farewell message for later
  def new_farewell(self):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a {self.role}"},
        {"role": "user", "content": f"In the voice of a {self.role}, give me a farewell message."}
      ]
    )
    farewell = response.choices[0].message.content
    self.farewell = farewell
    self.past_responses.append(farewell)


    

## Here we save old characters and their new question and outro.
###### Honestly? This is just so I can save some precious tokens for the API queries... Can you blame me?
  def saved_past_roles(self):
    self._past_lives[self.role] = [self.question, self.intro, self.outro, self.farewell]



### Want to view our past lives? Here we go.
  def view_past_lives(self):
    lives = list(self.past_lives.keys())
    if len(lives) == 1:
      print(lack_of_travels)
    else:
      print('================================')
      for i in range(len(lives)):
       print(f'''{i + 1}) {lives[i]}''')
    return lives  


### Ever wish you could relive your (past)life? Well here, you can!
### Again... just doing this to save API tokens...
  def reincarnation(self):
    lives = self.view_past_lives()
    print('================================')
    print('===========Q to return==========')
    user_input = input('============Number?============')
    while user_input.isnumeric == False or lives[int(user_input) - 1] == False:
      print(self.outro)
      self.reincarnation()
    role = lives[int(user_input)-1] 
    self.role = role
    self.question = self._past_lives[role][0]
    self.intro = self._past_lives[role][1]
    self.outro = self._past_lives[role][2]
    self.farewell = self._past_lives[role][3]




### No Volunteers? So be it...
  def chopping_block(self):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a {self.role}"},
        {"role": "user", "content": f"In the voice of a {self.role}, choose only one name from this list: {CHOPPING_BLOCK}, give me a single name."}
      ]
    )
    self.translate_response(response)



      




#### Here's our window into this demo!!

  def start(self):
    print(f'''
================================
1. Have Shakespeare explain OOP?
2. Change your character
3. Cast a new question or demand
4. View past lives
5. Reincarnation?
6. Exit
777. Spin the wheel 
          ''') 
    choice = input(f'''================================
{self.intro}\n================================\n>>>>''')
    match choice:
      case '1':

        self.ask_Shakepeare()
        self.start()
  
      case '2':
        self.make_a_role()
        self.start()
  
      case '3':
        self.ask_a_question()
        self.start()

      case '4':
        self.view_past_lives()
        self.start()

      case '5':
        self.reincarnation()
        self.start()

      case '6':
        print(f'{self.farewell}')
        return
      
      case '777':
        self.chopping_block()
        self.start()
      
      case _:
        print(f'{self.outro}')
        self.start()




bill = Bard()
bill.start()
