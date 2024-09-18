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

Para testear usar:
```zsh
pytest -s test_leave_room.py --disable-warnings
```

Pequeña descripcion:
Main.py contiene toda la estructura del feature, hace 2 comprobaciones para corroborar la veracidad de los datos recibidos desde el endpoint y luego procede a ejecutarlos
Puede mandar 2 tipos de mensaje, HTTP200 OK y HTTP500 ServerInternalError

Test_leave_room.py contiene varios tests para poder probar el correcto funcionamiento de todos los pasos en main.py

