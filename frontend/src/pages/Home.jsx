export default function Home() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
            {/* Hero Section */}
            <div className="container mx-auto px-4 py-16">
                <div className="text-center mb-12">
                    <h1 className="text-5xl font-bold text-primary-600 mb-4">
                        ASOPADEL BARINAS
                    </h1>
                    <p className="text-xl text-gray-700 mb-8">
                        Asociación de Pádel de Barinas
                    </p>
                </div>

                {/* Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                    <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
                        <div className="text-4xl mb-4">🏆</div>
                        <h3 className="text-2xl font-semibold text-primary-600 mb-3">
                            Torneos
                        </h3>
                        <p className="text-gray-600">
                            Participa en nuestros torneos de pádel y compite con los mejores jugadores de la región.
                        </p>
                    </div>

                    <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
                        <div className="text-4xl mb-4">🎾</div>
                        <h3 className="text-2xl font-semibold text-primary-600 mb-3">
                            Canchas
                        </h3>
                        <p className="text-gray-600">
                            Reserva nuestras canchas de última generación para tus partidos y entrenamientos.
                        </p>
                    </div>

                    <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
                        <div className="text-4xl mb-4">👥</div>
                        <h3 className="text-2xl font-semibold text-primary-600 mb-3">
                            Comunidad
                        </h3>
                        <p className="text-gray-600">
                            Únete a nuestra comunidad de jugadores y árbitros apasionados por el pádel.
                        </p>
                    </div>
                </div>

                {/* CTA Section */}
                <div className="text-center bg-white p-12 rounded-xl shadow-lg">
                    <h2 className="text-3xl font-bold text-gray-800 mb-4">
                        ¿Listo para comenzar?
                    </h2>
                    <p className="text-gray-600 mb-8">
                        Inicia sesión para acceder a todas las funcionalidades
                    </p>
                    <a
                        href="/login"
                        className="inline-block bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 transition shadow-lg hover:shadow-xl"
                    >
                        Iniciar Sesión
                    </a>
                </div>
            </div>

            {/* Footer */}
            <footer className="bg-primary-600 text-white py-8 mt-16">
                <div className="container mx-auto px-4 text-center">
                    <p>&copy; 2025 ASOPADEL Barinas. Todos los derechos reservados.</p>
                </div>
            </footer>
        </div>
    );
}
