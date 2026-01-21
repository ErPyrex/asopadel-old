"""
Django management command to populate the database with sample data.
This creates test users, tournaments, matches, news, and courts.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from users.models import Usuario
from competitions.models import Categoria, Torneo, Partido, EstadisticaJugador
from facilities.models import Cancha, ReservaCancha
from blog.models import Noticia


class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🗑️  Limpiando datos existentes...'))
        
        # Limpiar datos existentes (excepto superusuarios)
        Partido.objects.all().delete()
        Torneo.objects.all().delete()
        ReservaCancha.objects.all().delete()
        Cancha.objects.all().delete()
        Noticia.objects.all().delete()
        EstadisticaJugador.objects.all().delete()
        Usuario.objects.filter(is_superuser=False).delete()
        Categoria.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✅ Datos limpiados'))

        # 1. Crear Categorías
        self.stdout.write('📁 Creando categorías...')
        categorias = []
        for nombre, desc in [
            ('Juvenil', 'Jugadores menores de 18 años'),
            ('Adulto', 'Jugadores de 18 a 55 años'),
            ('Senior', 'Jugadores mayores de 55 años'),
            ('Mixto', 'Equipos mixtos (hombre y mujer)'),
        ]:
            cat = Categoria.objects.create(nombre=nombre, descripcion=desc)
            categorias.append(cat)
        self.stdout.write(self.style.SUCCESS(f'   Creadas {len(categorias)} categorías'))

        # 2. Crear Canchas
        self.stdout.write('🏟️  Creando canchas...')
        canchas_data = [
            ('Cancha Central', 'Av. Principal, Barinas', 'disponible', 25.00, 'La cancha principal con iluminación LED profesional'),
            ('Cancha Norte', 'Urb. Los Próceres, Barinas', 'disponible', 20.00, 'Cancha cubierta con césped sintético'),
            ('Cancha Sur', 'Sector El Estadio, Barinas', 'disponible', 18.00, 'Cancha al aire libre con vista panorámica'),
            ('Cancha Elite', 'CC Las Vegas, Barinas', 'disponible', 35.00, 'Cancha premium con aire acondicionado y servicio VIP'),
            ('Cancha Familiar', 'Parque Los Mangos, Barinas', 'mantenimiento', 15.00, 'En mantenimiento hasta febrero'),
        ]
        canchas = []
        for nombre, ubicacion, estado, precio, desc in canchas_data:
            cancha = Cancha.objects.create(
                nombre=nombre,
                ubicacion=ubicacion,
                estado=estado,
                precio_hora=precio,
                descripcion=desc,
                horario_apertura='08:00',
                horario_cierre='22:00'
            )
            canchas.append(cancha)
        self.stdout.write(self.style.SUCCESS(f'   Creadas {len(canchas)} canchas'))

        # 3. Crear Árbitros
        self.stdout.write('⚖️  Creando árbitros...')
        arbitros_data = [
            ('V12345678', 'Carlos', 'Mendoza', 'carlos.mendoza@asopadel.com', '04141234567'),
            ('V23456789', 'María', 'González', 'maria.gonzalez@asopadel.com', '04242345678'),
            ('V34567890', 'Pedro', 'Ramírez', 'pedro.ramirez@asopadel.com', '04163456789'),
        ]
        arbitros = []
        for cedula, nombre, apellido, email, telefono in arbitros_data:
            arbitro = Usuario.objects.create_user(
                cedula=cedula,
                password='asopadel2024',
                first_name=nombre,
                last_name=apellido,
                email=email,
                telefono=telefono,
                es_arbitro=True,
                es_jugador=False
            )
            arbitros.append(arbitro)
        self.stdout.write(self.style.SUCCESS(f'   Creados {len(arbitros)} árbitros'))

        # 3.5 Crear Admins normales (no superusuarios)
        self.stdout.write('👤 Creando administradores...')
        admins_data = [
            ('V11111111', 'Admin', 'Prueba', 'admin.prueba@asopadel.com', '04141111111'),
            ('V22222222', 'Gestor', 'ASOPADEL', 'gestor@asopadel.com', '04142222222'),
        ]
        admins = []
        for cedula, nombre, apellido, email, telefono in admins_data:
            admin_user = Usuario.objects.create_user(
                cedula=cedula,
                password='admin2024',
                first_name=nombre,
                last_name=apellido,
                email=email,
                telefono=telefono,
                es_admin_aso=True,
                es_arbitro=False,
                es_jugador=False
            )
            admins.append(admin_user)
        self.stdout.write(self.style.SUCCESS(f'   Creados {len(admins)} administradores'))

        # 4. Crear Jugadores
        self.stdout.write('🎾 Creando jugadores...')
        jugadores_data = [
            # Juveniles
            ('V45678901', 'Andrés', 'López', 'andres.lopez@email.com', '04121111111', 'juvenil', 1500),
            ('V56789012', 'Sofía', 'Martínez', 'sofia.martinez@email.com', '04122222222', 'juvenil', 1400),
            ('V67890123', 'Diego', 'Hernández', 'diego.hernandez@email.com', '04123333333', 'juvenil', 1350),
            ('V78901234', 'Valentina', 'García', 'valentina.garcia@email.com', '04124444444', 'juvenil', 1300),
            # Adultos
            ('V89012345', 'Roberto', 'Pérez', 'roberto.perez@email.com', '04145555555', 'adulto', 1800),
            ('V90123456', 'Carolina', 'Rodríguez', 'carolina.rodriguez@email.com', '04146666666', 'adulto', 1750),
            ('V01234567', 'Fernando', 'Sánchez', 'fernando.sanchez@email.com', '04147777777', 'adulto', 1650),
            ('V11234567', 'Patricia', 'Torres', 'patricia.torres@email.com', '04148888888', 'adulto', 1600),
            ('V12234567', 'Alejandro', 'Vargas', 'alejandro.vargas@email.com', '04149999999', 'adulto', 1550),
            ('V13234567', 'Gabriela', 'Moreno', 'gabriela.moreno@email.com', '04140000001', 'adulto', 1500),
            ('V14234567', 'Javier', 'Díaz', 'javier.diaz@email.com', '04140000002', 'adulto', 1450),
            ('V15234567', 'Daniela', 'Flores', 'daniela.flores@email.com', '04140000003', 'adulto', 1400),
            # Seniors
            ('V16234567', 'Manuel', 'Castillo', 'manuel.castillo@email.com', '04161111111', 'senior', 1700),
            ('V17234567', 'Rosa', 'Jiménez', 'rosa.jimenez@email.com', '04162222222', 'senior', 1650),
            ('V18234567', 'Francisco', 'Ruiz', 'francisco.ruiz@email.com', '04163333333', 'senior', 1600),
            ('V19234567', 'Elena', 'Navarro', 'elena.navarro@email.com', '04164444444', 'senior', 1550),
        ]
        jugadores = []
        for cedula, nombre, apellido, email, telefono, categoria, ranking in jugadores_data:
            jugador = Usuario.objects.create_user(
                cedula=cedula,
                password='jugador2024',
                first_name=nombre,
                last_name=apellido,
                email=email,
                telefono=telefono,
                es_jugador=True,
                es_arbitro=False,
                categoria_jugador=categoria,
                ranking=ranking
            )
            jugadores.append(jugador)
        self.stdout.write(self.style.SUCCESS(f'   Creados {len(jugadores)} jugadores'))

        # 5. Crear Torneos
        self.stdout.write('🏆 Creando torneos...')
        today = timezone.now().date()
        torneos_data = [
            # Torneos próximos
            ('Torneo Apertura 2026', 'El torneo más esperado del año. ¡Inscríbete ahora!', today + timedelta(days=30), today + timedelta(days=37), categorias[1], 'Primer lugar: Bs. 5,000 | Segundo lugar: Bs. 2,500'),
            ('Copa Juvenil Barinas', 'Torneo para las nuevas promesas del pádel barinés.', today + timedelta(days=45), today + timedelta(days=52), categorias[0], 'Trofeos y medallas para los 3 primeros lugares'),
            ('Campeonato Senior', 'Experiencia y técnica se unen en este torneo exclusivo.', today + timedelta(days=60), today + timedelta(days=65), categorias[2], 'Premios en efectivo y reconocimientos'),
            # Torneos en curso
            ('Liga de Verano 2026', 'Torneo regular con partidos semanales durante todo el verano.', today - timedelta(days=7), today + timedelta(days=21), categorias[1], 'Premio acumulado según participación'),
            # Torneos finalizados
            ('Torneo Clausura 2025', 'Gran final del año pasado con récord de participación.', today - timedelta(days=60), today - timedelta(days=53), categorias[1], 'Entregados premios por Bs. 10,000'),
            ('Copa Navideña', 'Torneo especial de fin de año.', today - timedelta(days=30), today - timedelta(days=25), categorias[3], 'Canastas navideñas y premios especiales'),
        ]
        torneos = []
        for nombre, desc, inicio, fin, cat, premios in torneos_data:
            torneo = Torneo.objects.create(
                nombre=nombre,
                descripcion=desc,
                fecha_inicio=inicio,
                fecha_fin=fin,
                categoria=cat,
                premios=premios,
                arbitro=random.choice(arbitros)
            )
            # Inscribir jugadores aleatorios
            jugadores_cat = [j for j in jugadores if j.categoria_jugador == cat.nombre.lower() or cat.nombre == 'Mixto']
            if not jugadores_cat:
                jugadores_cat = random.sample(jugadores, min(6, len(jugadores)))
            for j in random.sample(jugadores_cat, min(len(jugadores_cat), random.randint(4, 8))):
                torneo.jugadores_inscritos.add(j)
            torneos.append(torneo)
        self.stdout.write(self.style.SUCCESS(f'   Creados {len(torneos)} torneos'))

        # 6. Crear Partidos
        self.stdout.write('🎯 Creando partidos...')
        partidos_creados = 0
        horas_partido = ['09:00', '11:00', '14:00', '16:00', '18:00', '20:00']
        
        # Partidos para torneos
        for torneo in torneos:
            inscritos = list(torneo.jugadores_inscritos.all())
            if len(inscritos) >= 4:
                num_partidos = min(4, len(inscritos) // 2)
                for i in range(num_partidos):
                    fecha = torneo.fecha_inicio + timedelta(days=random.randint(0, (torneo.fecha_fin - torneo.fecha_inicio).days))
                    
                    # Determinar estado según fechas
                    if fecha < today:
                        estado = 'finalizado'
                        marcador = f"{random.randint(10, 21)}-{random.randint(5, 18)}"
                        ganador = random.choice([1, 2])
                    elif fecha == today:
                        estado = 'confirmado'
                        marcador = ''
                        ganador = None
                    else:
                        estado = 'pendiente'
                        marcador = ''
                        ganador = None
                    
                    partido = Partido.objects.create(
                        torneo=torneo,
                        cancha=random.choice([c for c in canchas if c.estado != 'mantenimiento']),
                        fecha=fecha,
                        hora=random.choice(horas_partido),
                        arbitro=random.choice(arbitros),
                        estado=estado,
                        marcador=marcador,
                        equipo_ganador=ganador
                    )
                    # Asignar equipos (2v2)
                    equipo1 = random.sample(inscritos, 2)
                    restantes = [j for j in inscritos if j not in equipo1]
                    equipo2 = random.sample(restantes, min(2, len(restantes)))
                    
                    for j in equipo1:
                        partido.equipo1.add(j)
                    for j in equipo2:
                        partido.equipo2.add(j)
                    
                    partidos_creados += 1

        # Partidos casuales (sin torneo)
        for i in range(5):
            fecha = today + timedelta(days=random.randint(-10, 15))
            estado = 'finalizado' if fecha < today else ('confirmado' if fecha == today else 'pendiente')
            
            partido = Partido.objects.create(
                torneo=None,
                cancha=random.choice([c for c in canchas if c.estado != 'mantenimiento']),
                fecha=fecha,
                hora=random.choice(horas_partido),
                arbitro=random.choice(arbitros) if random.random() > 0.3 else None,
                estado=estado,
                marcador=f"{random.randint(10, 21)}-{random.randint(5, 18)}" if estado == 'finalizado' else '',
                equipo_ganador=random.choice([1, 2]) if estado == 'finalizado' else None
            )
            equipo1 = random.sample(jugadores, 2)
            equipo2 = random.sample([j for j in jugadores if j not in equipo1], 2)
            for j in equipo1:
                partido.equipo1.add(j)
            for j in equipo2:
                partido.equipo2.add(j)
            partidos_creados += 1

        self.stdout.write(self.style.SUCCESS(f'   Creados {partidos_creados} partidos'))

        # 7. Crear Noticias
        self.stdout.write('📰 Creando noticias...')
        
        # Crear admin de prueba si no existe ninguno
        admin = Usuario.objects.filter(is_superuser=True).first()
        if not admin:
            admin = Usuario.objects.create_superuser(
                cedula='V00000001',
                password='admin2024',
                first_name='Admin',
                last_name='ASOPADEL',
                email='admin@asopadel.com',
                telefono='04140000000'
            )
            self.stdout.write(self.style.SUCCESS('   Creado admin de prueba (cedula: V00000001, password: admin2024)'))
        
        noticias_data = [
            ('¡Inscripciones abiertas para el Torneo Apertura 2026!', 
             'Las inscripciones para el torneo más esperado del año ya están abiertas. No pierdas la oportunidad de participar en esta competencia que reunirá a los mejores jugadores de la región.\n\nEl torneo contará con premios en efectivo y trofeos para los primeros lugares. Las inscripciones estarán disponibles hasta una semana antes del inicio del evento.\n\n¡No te lo pierdas!'),
            ('Nuevas canchas iluminadas para partidos nocturnos',
             'ASOPADEL Barinas se complace en anunciar la instalación de un nuevo sistema de iluminación LED en la Cancha Central. Este sistema de última generación permite jugar partidos nocturnos con excelente visibilidad.\n\nLa inversión forma parte de nuestro compromiso continuo con la mejora de las instalaciones deportivas.'),
            ('Resultados del Torneo Clausura 2025',
             'El Torneo Clausura 2025 llegó a su fin con una gran final emocionante. Felicitamos a todos los participantes y especialmente a los ganadores.\n\nAgradecemos a todos los jugadores, árbitros y voluntarios que hicieron posible este evento. ¡Nos vemos en el próximo torneo!'),
            ('Clínicas de pádel para principiantes',
             'ASOPADEL organiza clínicas de pádel para principiantes todos los sábados de 8:00 AM a 10:00 AM. Las clases son gratuitas para miembros y tienen un costo accesible para no miembros.\n\nVen a aprender los fundamentos del pádel con nuestros instructores certificados.'),
            ('Mantenimiento programado en Cancha Familiar',
             'Informamos a nuestra comunidad que la Cancha Familiar estará en mantenimiento durante el mes de febrero. Esto incluye renovación del césped sintético y mejoras en el sistema de drenaje.\n\nPedimos disculpas por las molestias y agradecemos su comprensión.'),
        ]
        for titulo, cuerpo in noticias_data:
            Noticia.objects.create(
                titulo=titulo,
                cuerpo=cuerpo,
                autor=admin
            )
        self.stdout.write(self.style.SUCCESS(f'   Creadas {len(noticias_data)} noticias'))

        # 8. Crear Estadísticas para jugadores
        self.stdout.write('📊 Creando estadísticas...')
        for jugador in jugadores:
            cat = categorias[0] if jugador.categoria_jugador == 'juvenil' else (
                categorias[2] if jugador.categoria_jugador == 'senior' else categorias[1]
            )
            # Generar estadísticas coherentes: victorias + derrotas = partidos_jugados
            partidos_jugados = random.randint(10, 35)
            victorias = random.randint(2, partidos_jugados - 2)  # Al menos 2 derrotas
            derrotas = partidos_jugados - victorias
            
            EstadisticaJugador.objects.create(
                jugador=jugador,
                categoria=cat,
                partidos_jugados=partidos_jugados,
                victorias=victorias,
                derrotas=derrotas
            )
        self.stdout.write(self.style.SUCCESS(f'   Creadas estadísticas para {len(jugadores)} jugadores'))

        # Resumen final
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('🎉 ¡Base de datos poblada exitosamente!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write(f'📁 Categorías: {Categoria.objects.count()}')
        self.stdout.write(f'🏟️  Canchas: {Cancha.objects.count()}')
        self.stdout.write(f'👤 Administradores: {Usuario.objects.filter(es_admin_aso=True).count()}')
        self.stdout.write(f'⚖️  Árbitros: {Usuario.objects.filter(es_arbitro=True).count()}')
        self.stdout.write(f'🎾 Jugadores: {Usuario.objects.filter(es_jugador=True).count()}')
        self.stdout.write(f'🏆 Torneos: {Torneo.objects.count()}')
        self.stdout.write(f'🎯 Partidos: {Partido.objects.count()}')
        self.stdout.write(f'📰 Noticias: {Noticia.objects.count()}')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('📌 Credenciales de prueba:'))
        self.stdout.write('   Administradores: contraseña "admin2024"')
        self.stdout.write('   Árbitros: contraseña "asopadel2024"')
        self.stdout.write('   Jugadores: contraseña "jugador2024"')
