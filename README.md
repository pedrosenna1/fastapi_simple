# fastapi_simple
API simples de fastapi com dados mockados

Gerando secret para o JWT:

Crie um script  e coloque isto:

```python
import secrets

print(secrets.token_hex())
```

**copie o secret gerado**

Crie um arquivo .env e dentro coloque o secret gerado:

SECRET_JWT=[COLOQUE AQUI SUA SECRET)


## Exemplo básico de uso Bearer Token ( funcionando no swagger)

### Fazer o import dessa bibliotecas:

```python
from fastapi import FastAPI,HTTPException,Header,Depends
from pydantic import BaseModel
from typing import Optional,Union
import jwt
from datetime import datetime, timedelta,timezone
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
```

### Iniciar o app, secret( que deve estar no .env) e oauth2_scheme

O Oauth2_scheme devemos passar o caminho da rota de geração do token

```python
app = FastAPI()
secret = '3648334f253c4e5f98254395f95a79ee304488cdf72818772b0485b06f0557b8'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/Authorization", scopes={})
```

### Rota de criação do Token:

```python
@app.post('/api/Authorization')
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
	try:
		# verificação dos dados do usuario:
		# acessamos via form_data.username e form_data.password
		# CRIAÇÂO DO PAYLOAD - USAR UTC SEMPRE!
		payload = {
		            'email': form_data.username,
		            'exp': datetime.now(timezone.utc) + timedelta(minutes=15)
		        }
		token = jwt.encode(payload=payload,key=secret,algorithm="HS256")
		return {'access_token': token,
		                'token_type': 'bearer'}
		                
	raise HTTPException(status_code=401,detail='Credenciais inválidas')
```

### Rota de GET com possiveis args:

```python
class FilterCampaign(BaseModel):
    id: Optional[int] = None
    limit: Optional[int] = None

@app.get('/api/get_campaign')
async def get_campanha(filters: FilterCampaign = Depends(), token: str = Depends(oauth2_scheme)):
	try:
	        
	        jwt.decode(token,secret,algorithms=["HS256"])
	        filters = filters.model_dump(exclude_none=True)
		      if not filters:
            return mock_dados
          if 'id' in filters:
                for campanha in mock_dados:
                    if campanha['id'] == filters['id']:
                        return campanha
                    break
        if 'limit' in filters:
            dados_limit = []
            for i in range(filters['limit']):
                
                mock_dados[i]
                dados_limit.append(mock_dados[i])
            return {'success': True,
                    'data': dados_limit}

    except jwt.ExpiredSignatureError:
        return {'message': 'Token expirado'}
    else:
        raise HTTPException(status_code=401,detail='Token inválido')
```
