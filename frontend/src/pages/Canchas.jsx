import { useQuery } from '@tanstack/react-query';
import { canchaService } from '../services/dataService';

export default function Canchas() {
    const { data, isLoading, error } = useQuery({
        queryKey: ['canchas'],
        queryFn: canchaService.getAll,
    });

    if (isLoading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="text-center">Cargando canchas...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                    Error al cargar canchas: {error.message}
                </div>
            </div>
        );
    }

    const canchas = data?.results || data || [];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-4xl font-bold text-gray-800">Canchas</h1>
            </div>

            {canchas.length === 0 ? (
                <div className="bg-gray-100 p-8 rounded-lg text-center">
                    <p className="text-gray-600">No hay canchas disponibles</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {canchas.map((cancha) => (
                        <div
                            key={cancha.id}
                            className="bg-white rounded-lg shadow-md hover:shadow-xl transition p-6"
                        >
                            <h3 className="text-xl font-semibold text-primary-600 mb-2">
                                {cancha.nombre}
                            </h3>
                            {cancha.descripcion && (
                                <p className="text-gray-600 mb-4">{cancha.descripcion}</p>
                            )}
                            <div className="flex items-center justify-between">
                                <span className={`px-3 py-1 rounded-full text-sm ${cancha.disponible
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-red-100 text-red-800'
                                    }`}>
                                    {cancha.disponible ? 'Disponible' : 'No disponible'}
                                </span>
                                {cancha.reservas_activas !== undefined && (
                                    <span className="text-sm text-gray-500">
                                        {cancha.reservas_activas} reservas
                                    </span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
