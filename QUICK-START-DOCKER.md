# 🚀 Inicio Rápido con Docker - ImportAR# 🚀 INICIO RÁPIDO - Crear Imagen Docker



## ✅ Todo Listo para Docker## ✅ SÍ, YA PUEDES CREAR LA IMAGEN COMPLETA DEL PROYECTO



El proyecto está completamente configurado para ejecutarse con Docker.---



---## 📦 Lo que tenemos listo:



## 🎯 Opción 1: Proyecto Completo (Recomendado)1. ✅ **Dockerfile refactorizado** (multi-stage, optimizado)

2. ✅ **pyproject.toml** actualizado con gunicorn

Levanta **Frontend + Backend + MySQL** desde la raíz:3. ✅ **uv.lock** actualizado con todas las dependencias

4. ✅ **.dockerignore** para optimizar build

```bash5. ✅ **docker-compose.yml** para orquestar app + DB

# Desde C:\Users\Catalan\Documents\GitHub6. ✅ **Endpoint /health** para health checks

cd C:\Users\Catalan\Documents\GitHub7. ✅ **Código fuente completo** en /app

docker-compose up -d --build

```---



Esto levanta:## 🎯 Comando Simple para Crear la Imagen:

- ✅ Frontend en http://localhost

- ✅ Backend en http://localhost:5000```powershell

- ✅ MySQL en puerto 3307# En el directorio del proyecto:

docker build -t importar:latest .

---```



## 🔧 Opción 2: Solo Backend + MySQL### Eso es todo! ✨



Si solo necesitas el backend:---



```bash## 🔥 Comando Recomendado (con Docker Compose):

# Desde ImportAR/

cd ImportAR```powershell

docker-compose up -d --build# Crea la imagen Y levanta todo el stack (app + MySQL)

```docker-compose up -d --build

```

Esto levanta:

- ✅ Backend en http://localhost:5000Luego verifica:

- ✅ MySQL en puerto 3307```powershell

# Ver logs

---docker-compose logs -f app



## ⚡ Verificación Rápida# Probar health

curl http://localhost:5000/api/v1/health

```bash

# Ver contenedores corriendo# O abrir en navegador

docker psstart http://localhost:5000/api/v1/health

```

# Ver logs

docker-compose logs -f---



# Probar backend## 📋 Paso a Paso Completo:

curl http://localhost:5000/api/v1/health

### 1️⃣ Preparación (SOLO SI NO EXISTE .env)

# O abrir en navegador```powershell

start http://localhost:5000/api/v1/health# Copiar variables de entorno

```cp .env.example .env

```

---

### 2️⃣ Construir

## 🛑 Detener Todo```powershell

# Opción A: Solo imagen

```bashdocker build -t importar:latest .

# Detener contenedores

docker-compose down# Opción B: Con docker-compose (RECOMENDADO)

docker-compose up -d --build

# Detener y eliminar datos de MySQL```

docker-compose down -v

```### 3️⃣ Verificar

```powershell

---# Ver imágenes

docker images importar

## 📊 Comandos Útiles

# Ver contenedores corriendo

```bashdocker ps

# Reconstruir sin cache

docker-compose build --no-cache# Ver logs

docker logs importar-app

# Ver logs de un servicio específico# o

docker-compose logs -f backenddocker-compose logs -f

```

# Ejecutar comando en el contenedor

docker exec -it importar-backend bash### 4️⃣ Probar

```powershell

# Reiniciar un servicio# Health check

docker-compose restart backendcurl http://localhost:5000/api/v1/health

```

# Endpoint principal

---curl http://localhost:5000/api/v1/

```

## 🐛 Troubleshooting

---

### Puerto ocupado

```bash## ⏱️ Tiempos Esperados:

# Cambiar el puerto en docker-compose.yml

# "5000:5000" → "5001:5000"- **Primera construcción:** 5-15 minutos

```- **Construcciones posteriores:** 1-3 minutos (gracias al cache)

- **Tamaño de imagen final:** ~200-400 MB

### MySQL no inicia

```bash---

# Ver logs

docker-compose logs mysql## 🎉 ¿Qué pasa después del build?



# Eliminar volumen y reiniciarUna vez construida la imagen:

docker-compose down -v

docker-compose up -d✅ Puedes **ejecutarla localmente** con Docker

```✅ Puedes **subirla a Docker Hub** o registro privado

✅ Puedes **deployarla en cualquier servidor** con Docker

### Backend no conecta a MySQL✅ Puedes **usarla en Kubernetes**, AWS ECS, etc.

```bash✅ La imagen es **completamente portable**

# Esperar a que MySQL esté listo (healthcheck)

docker-compose logs backend---

```

## 🐛 Si algo falla:

---

### Error común #1: Docker no está corriendo

## 📝 Estructura de Docker```powershell

# Solución: Inicia Docker Desktop

``````

Backend Dockerfile: Multi-stage optimizado con uv

MySQL: Imagen oficial 8.0### Error común #2: Puerto 5000 ocupado

Volúmenes: Persistencia de datos MySQL```powershell

Network: Red bridge para comunicación interna# Solución: Cambia el puerto en docker-compose.yml

```# o detén el proceso que usa el puerto 5000

```

---

### Error común #3: Dependencias no resuelven

**¡Listo! Tu aplicación estará corriendo en minutos. 🚀**```powershell

# Solución: Actualiza el lock
uv lock --upgrade
```

### Script de diagnóstico:
```powershell
# Si tienes problemas, ejecuta:
.\test-docker-build.ps1
```

---

## 💡 Tips:

1. **Usa docker-compose** para desarrollo (incluye MySQL)
2. **Usa docker build** solo si necesitas la imagen standalone
3. **El .dockerignore** hace que el build sea más rápido
4. **La primera construcción descarga todo**, las siguientes son más rápidas
5. **No necesitas tener Python instalado** en el servidor de producción

---

## 🚀 Despliegue Rápido:

```powershell
# Local
docker-compose up -d

# Producción (ejemplo)
docker tag importar:latest tu-registro/importar:v1.0
docker push tu-registro/importar:v1.0
```

---

## ✅ RESPUESTA FINAL:

# SÍ, PUEDES CREAR LA IMAGEN AHORA MISMO

Ejecuta:
```powershell
docker build -t importar:latest .
```

O mejor:
```powershell
docker-compose up -d --build
```

¡Y listo! 🎉
