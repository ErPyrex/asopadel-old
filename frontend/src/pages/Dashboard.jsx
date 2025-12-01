export default function Dashboard() {
    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-6">Dashboard</h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-xl font-semibold text-primary-600 mb-2">Torneos</h3>
                    <p className="text-gray-600">Gestiona los torneos activos</p>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-xl font-semibold text-primary-600 mb-2">Canchas</h3>
                    <p className="text-gray-600">Administra las canchas disponibles</p>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-xl font-semibold text-primary-600 mb-2">Usuarios</h3>
                    <p className="text-gray-600">Gestiona los usuarios del sistema</p>
                </div>
            </div>
        </div>
    );
}
