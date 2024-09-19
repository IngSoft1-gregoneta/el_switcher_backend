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

Levantar servidor en `el_switcher_backend/app`
```zsh
fastapi dev main.py
```
Levantar servidor recargable
```sh
uvicorn main:app --reload
```
Correr tests en `el_switcher_backend` 
(asegurarse de estar "parado" en dicha carpeta)
```sh
./run_tests.sh
```
