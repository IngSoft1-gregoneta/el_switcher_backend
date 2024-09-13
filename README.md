# Backend
Primero crear entorno virtual y activarlo

```zsh
cd backend
python3 -m venv ./venv
source venv/bin/activate
```

Instalar dependencias
```zsh
pip install -r requirements.txt
```

Levantar servidor en `backend/app`
```zsh
fastapi dev main.py
```


