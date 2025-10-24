# 🚀 INICIO RÁPIDO - Crear Imagen Docker

## ✅ SÍ, YA PUEDES CREAR LA IMAGEN COMPLETA DEL PROYECTO

---

## 📦 Lo que tenemos listo:

1. ✅ **Dockerfile refactorizado** (multi-stage, optimizado)
2. ✅ **pyproject.toml** actualizado con gunicorn
3. ✅ **uv.lock** actualizado con todas las dependencias
4. ✅ **.dockerignore** para optimizar build
5. ✅ **docker-compose.yml** para orquestar app + DB
6. ✅ **Endpoint /health** para health checks
7. ✅ **Código fuente completo** en /app

---

## 🎯 Comando Simple para Crear la Imagen:

```powershell
# En el directorio del proyecto:
docker build -t importar:latest .
```

### Eso es todo! ✨

---

## 🔥 Comando Recomendado (con Docker Compose):

```powershell
# Crea la imagen Y levanta todo el stack (app + MySQL)
docker-compose up -d --build
```

Luego verifica:
```powershell
# Ver logs
docker-compose logs -f app

# Probar health
curl http://localhost:5000/api/v1/health

# O abrir en navegador
start http://localhost:5000/api/v1/health
```

---

## 📋 Paso a Paso Completo:

### 1️⃣ Preparación (SOLO SI NO EXISTE .env)
```powershell
# Copiar variables de entorno
cp .env.example .env
```

### 2️⃣ Construir
```powershell
# Opción A: Solo imagen
docker build -t importar:latest .

# Opción B: Con docker-compose (RECOMENDADO)
docker-compose up -d --build
```

### 3️⃣ Verificar
```powershell
# Ver imágenes
docker images importar

# Ver contenedores corriendo
docker ps

# Ver logs
docker logs importar-app
# o
docker-compose logs -f
```

### 4️⃣ Probar
```powershell
# Health check
curl http://localhost:5000/api/v1/health

# Endpoint principal
curl http://localhost:5000/api/v1/
```

---

## ⏱️ Tiempos Esperados:

- **Primera construcción:** 5-15 minutos
- **Construcciones posteriores:** 1-3 minutos (gracias al cache)
- **Tamaño de imagen final:** ~200-400 MB

---

## 🎉 ¿Qué pasa después del build?

Una vez construida la imagen:

✅ Puedes **ejecutarla localmente** con Docker
✅ Puedes **subirla a Docker Hub** o registro privado
✅ Puedes **deployarla en cualquier servidor** con Docker
✅ Puedes **usarla en Kubernetes**, AWS ECS, etc.
✅ La imagen es **completamente portable**

---

## 🐛 Si algo falla:

### Error común #1: Docker no está corriendo
```powershell
# Solución: Inicia Docker Desktop
```

### Error común #2: Puerto 5000 ocupado
```powershell
# Solución: Cambia el puerto en docker-compose.yml
# o detén el proceso que usa el puerto 5000
```

### Error común #3: Dependencias no resuelven
```powershell
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
