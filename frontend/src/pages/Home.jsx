export default function Home() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
            {/* Hero Section */}
            <div className="container mx-auto px-4 py-8 sm:py-12 lg:py-16">
                <div className="text-center mb-8 sm:mb-12">
                    <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-primary-600 mb-4">
                        ASOPADEL BARINAS
                    </h1>
                    <p className="text-lg sm:text-xl lg:text-2xl text-gray-700 mb-8">
                        Asociación de Pádel de Barinas
                    </p>
                </div>

                {/* Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 mb-8 sm:mb-12">
                    <div className="bg-white p-6 sm:p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
                        <div className="text-4xl mb-4">🏆</div>
                        <h3 className="text-xl sm:text-2xl font-semibold text-primary-600 mb-3">
                            Torneos
                        </h3>
                        <p className="text-gray-600 text-sm sm:text-base">
                            Participa en nuestros torneos de pádel y compite con los mejores jugadores de la región.
                        </p>
                    </div>

                    <div className="bg-white p-6 sm:p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
                        <div className="text-4xl mb-4">🎾</div>
                        <h3 className="text-xl sm:text-2xl font-semibold text-primary-600 mb-3">
                            Canchas
                        </h3>
                        <p className="text-gray-600 text-sm sm:text-base">
                            Reserva nuestras canchas de última generación para tus partidos y entrenamientos.
                        </p>
                    </div>

                    <div className="bg-white p-6 sm:p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
                        <div className="text-4xl mb-4">👥</div>
                        <h3 className="text-xl sm:text-2xl font-semibold text-primary-600 mb-3">
                            Comunidad
                        </h3>
                        <p className="text-gray-600 text-sm sm:text-base">
                            Únete a nuestra comunidad de jugadores y árbitros apasionados por el pádel.
                        </p>
                    </div>
                </div>

                {/* CTA Section */}
                <div className="text-center bg-white p-8 sm:p-12 rounded-xl shadow-lg">
                    <h2 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-4">
                        ¿Listo para comenzar?
                    </h2>
                    <p className="text-gray-600 mb-6 sm:mb-8 text-sm sm:text-base">
                        Regístrate como jugador o árbitro y accede a todas las funcionalidades
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                        <a
                            href="/register"
                            className="w-full sm:w-auto inline-block bg-primary-600 text-white px-6 sm:px-8 py-3 sm:py-4 rounded-lg text-base sm:text-lg font-semibold hover:bg-primary-700 transition shadow-lg hover:shadow-xl"
                        >
                            Registrarse
                        </a>
                        <a
                            href="/login"
                            className="w-full sm:w-auto inline-block bg-white text-primary-600 border-2 border-primary-600 px-6 sm:px-8 py-3 sm:py-4 rounded-lg text-base sm:text-lg font-semibold hover:bg-primary-50 transition"
                        >
                            Iniciar Sesión
                        </a>
                    </div>
                </div>
            </div>

            {/* Footer */}
            <footer className="bg-primary-600 text-white py-6 sm:py-8 mt-12 sm:mt-16">
                <div className="container mx-auto px-4 text-center">
                    <p className="text-sm sm:text-base">&copy; 2025 ASOPADEL Barinas. Todos los derechos reservados.</p>
                </div>
            </footer>
        </div>
    );
}
