# ImportAR – Calculadora de Costos de Importación

Proyecto desarrollado para la materia **Diseño de Sistemas**.  
El sistema permite simular y administrar el costo de importar productos a Argentina, contemplando impuestos, aranceles, fletes y gastos asociados, con operaciones básicas de simulación y presupuestos.

---

## Descripción

El sistema está orientado a la gestión de cálculos de importación, permitiendo a los actores interactuar de la siguiente manera:

- **Usuario**:  
  Inicia simulaciones, carga precios FOB/CIF, consulta resultados y guarda presupuestos.

- **Administrador**:  
  Supervisa usuarios, parámetros fiscales y controla el correcto funcionamiento del sistema.

---

## Casos de Uso

1. Iniciar simulación.  
2. Generar presupuesto.  
3. Calcular gastos de importación.  
4. Consultar historial de simulaciones.  
5. Administrar parámetros fiscales.  

---

## Tecnologías Utilizadas

- **Lenguaje**: Python 3.11+  
- **Framework**: FastAPI  
- **Base de datos**: MySQL (servidor)  
- **Interfaz**: API REST + posible frontend React  
- **Contenedores**: Docker / Docker Compose  
- **IDE**: Visual Studio Code  
- **Control de versiones**: GitHub  
- **Metodología**: Scrum  

---

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/tuusuario/ImportAR.git
cd ImportAR
```

### 2. Configurar el entorno virtual de Python
```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Levantar la base de datos MySQL
> Puede usarse Docker para esto.

### 5. Ejecutar la aplicación
```bash
flask run
```

---

## Pasos para configurar tu entorno de trabajo con `uv`

1. Abrir PowerShell como administrador.
2. Instalar `uv`: 
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
3. Reiniciar la PC.
4. Abrir el proyecto en Visual Studio Code.
5. Abrir la terminal en VS Code.
6. Verificar que `uv` está instalado: 
   ```bash
   uv
   ```
7. Crear un entorno virtual con `uv`: 
   ```bash
   uv venv
   ```
8. Instalar dependencias necesarias: 
   ```bash
   uv add flask==3.1.1
   uv add python-dotenv==1.1.1
   ```
9. Para actualizar dependencias en el proyecto: 
   ```bash
   uv sync
   ```
10. Para agregar Flask-SQLAlchemy y mysql-connector-python: 
    ```bash
    uv add "Flask-SQLAlchemy==3.1.1"
    uv add 'mysql-connector-python==9.4.0'
    ```