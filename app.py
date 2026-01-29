from fastapi import FastAPI,HTTPException,Header,Depends
from pydantic import BaseModel
from typing import Optional,Union
import jwt
from datetime import datetime, timedelta,timezone
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import os


app = FastAPI()
secret = os.getenv('SECRET_JWT')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/Authorization", scopes={})


mock_dados_login = [
    {
        'username': 'Pedro',
        'email': 'pedro@gmail.com',
        'senha': 'pedro123'
    },
    {
        'username': 'Joao',
        'email': 'Joao@gmail.com',
        'senha': 'joao123'
    }
]

mock_dados = [
  {
    "id": 1,
    "name": "Campanha Verão 2025",
    "status": "ACTIVE",
    "channel": "PROGRAMMATIC",
    "start_date": "2025-01-10",
    "end_date": "2025-02-28",
    "impressions": 1250000,
    "clicks": 18400,
    "investment": 18500.50,
    "created_at": "2025-01-05T10:15:00"
  },
  {
    "id": 2,
    "name": "Lançamento Produto X",
    "status": "PAUSED",
    "channel": "DIRECT",
    "start_date": "2025-01-20",
    "end_date": "2025-03-15",
    "impressions": 780000,
    "clicks": 9600,
    "investment": 12200.00,
    "created_at": "2025-01-18T09:40:00"
  },
  {
    "id": 3,
    "name": "Always On Institucional",
    "status": "ACTIVE",
    "channel": "PROGRAMMATIC",
    "start_date": "2024-11-01",
    "end_date": "2025-12-31",
    "impressions": 4520000,
    "clicks": 51200,
    "investment": 54000.00,
    "created_at": "2024-10-28T14:10:00"
  },
  {
    "id": 4,
    "name": "Black Friday 2024",
    "status": "FINISHED",
    "channel": "PROGRAMMATIC",
    "start_date": "2024-11-20",
    "end_date": "2024-11-30",
    "impressions": 2980000,
    "clicks": 43600,
    "investment": 31000.75,
    "created_at": "2024-11-10T08:30:00"
  },
  {
    "id": 5,
    "name": "Campanha Regional Sul",
    "status": "ACTIVE",
    "channel": "DIRECT",
    "start_date": "2025-02-01",
    "end_date": "2025-04-30",
    "impressions": 420000,
    "clicks": 5800,
    "investment": 7600.00,
    "created_at": "2025-01-28T16:45:00"
  }
]




@app.post('/api/Authorization')
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    global mock_dados_login
    global secret
    for user in mock_dados_login:
        if user['email'] == form_data.username and user['senha'] == form_data.password:
            payload = {
                'email': form_data.username,
                'exp': datetime.now(timezone.utc) + timedelta(minutes=15)
            }
            token = jwt.encode(payload=payload,key=secret,algorithm="HS256")
            
            return {'access_token': token,
                    'token_type': 'bearer'}
            
    raise HTTPException(status_code=401,detail='Credenciais inválidas')


class FilterCampaign(BaseModel):
    id: Optional[int] = None
    limit: Optional[int] = None

@app.get('/api/campaigns')
async def get_campanha(filters: FilterCampaign = Depends(), token: str = Depends(oauth2_scheme)):
    global mock_dados
    
    try:
        
        jwt.decode(token,secret,algorithms=["HS256"])
        filters = filters.model_dump(exclude_none=True)
        if not filters:
            return mock_dados 
        if 'id' in filters:
                for campanha in mock_dados:
                    if campanha['id'] == filters['id']:
                        return campanha
                    
        if 'limit' in filters:
            dados_limit = []
            for i in range(filters['limit']):
                
                mock_dados[i]
                dados_limit.append(mock_dados[i])
            return {'success': True,
                    'data': dados_limit}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    else:
        raise HTTPException(status_code=401,detail='Token inválido')
    
        

