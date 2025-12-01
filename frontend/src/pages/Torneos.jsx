import { useQuery } from '@tanstack/react-query';
import { torneoService } from '../services/dataService';
import { Link } from 'react-router-dom';

export default function Torneos() {
    const { data, isLoading, error } = useQuery({
        queryKey: ['torneos'],
        queryFn: torneoService.getAll,
    });

    if (isLoading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="text-center">Cargando torneos...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                    Error al cargar torneos: {error.message}
                </div>
            </div>
        );
    }

    const torneos = data?.results || data || [];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-4xl font-bold text-gray-800">Torneos</h1>
            </div>

            {torneos.length === 0 ? (
                <div className="bg-gray-100 p-8 rounded-lg text-center">
                    <p className="text-gray-600">No hay torneos disponibles</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {torneos.map((torneo) => (
                        <div
                            key={torneo.id}
                            className="bg-white rounded-lg shadow-md hover:shadow-xl transition p-6"
                        >
                            <h3 className="text-xl font-semibold text-primary-600 mb-2">
                                {torneo.nombre}
                            </h3>
                            <p className="text-gray-600 mb-4 line-clamp-2">
                                {torneo.descripcion}
                            </p>
                            <div className="flex justify-between text-sm text-gray-500 mb-4">
                                <span>
                                    Inicio: {new Date(torneo.fecha_inicio).toLocaleDateString()}
                                </span>
                                <span className="capitalize font-medium">{torneo.estado}</span>
                            </div>
                            {torneo.total_partidos !== undefined && (
                                <div className="text-sm text-gray-500">
                                    Partidos: {torneo.total_partidos}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
