import sqlite3
import pandas as pd
from fastapi import FastAPI, Response, Request
import uvicorn
from typing import Optional
from pydantic import BaseModel
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
path = os.path.dirname(os.path.abspath(__file__))

# model for ai prediction
class JsonAIResponse(BaseModel):
	sender: str
	receiver:str
	text:str

# model for updating database
class JsonUpdateDatabase(BaseModel):
	name:str
	hooli_number:str
	contact_number:Optional[str] = None

# instantiate fastapi
app = FastAPI()
# slowapi limiter per user/ip
limiter = Limiter(key_func=get_remote_address, default_limits=["1/1second"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# chatterbot caching
chatbot = ChatBot('Vox',storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="/database.db")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
# text prediction and respose for ai 
@app.post('/v1/hooli/message/')
@limiter.shared_limit(limit_value="1/1second", scope='message') 
async def ai_predict(request: Request,inputRequest: JsonAIResponse):
	sender = inputRequest.sender
	receiver = inputRequest.receiver
	text = inputRequest.text
	response = chatbot.get_response(str(text))
	jsonResponse = {'msg':str(response)}
	return jsonResponse

# updating database
@app.put('/v1/hooli/message/{restaurant_id}')
async def update_db(inputRequest: JsonUpdateDatabase, restaurant_id:str):
	name = inputRequest.name
	hooli_number = inputRequest.hooli_number
	restaurant_id = restaurant_id
	contact_number = inputRequest.contact_number

	# update if the contact number is filled
	if contact_number is not None:
		contact_number = inputRequest.contact_number

	# connect to database
	con = sqlite3.connect(path + '/database.sqlite')
	df_restaurants = pd.read_sql_query('select * from restaurant', con)
	print(df_restaurants)
	df_restaurant_id = df_restaurants.loc[df_restaurants['id'] == restaurant_id]
	# if the id exist can update other columnbs
	if len(df_restaurant_id) == 1:
		df_restaurants.replace(df_restaurant_id['name'][0], name, inplace=True)
		df_restaurants.replace(df_restaurant_id['hooli_number'][0], hooli_number, inplace=True)
		if contact_number is not None:
			df_restaurants.replace(df_restaurant_id['contact_phone'][0], contact_number, inplace=True)
	# if not add into new row
	else:
		new_row = {'id':restaurant_id, 'hooli_number':hooli_number, 'name':name, 'contact_phone':contact_number}
		df_restaurants.append(new_row, ignore_index=True)

	
	df_restaurants.to_sql("restaurant", con, if_exists="replace", index=False)
	con.close()
	return Response(status_code=202)

if __name__ == "__main__":  
	uvicorn.run(app, host='0.0.0.0', port=8000)