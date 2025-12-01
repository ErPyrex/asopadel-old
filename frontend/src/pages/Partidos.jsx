import { useQuery } from '@tanstack/react-query';
import { partidoService } from '../services/dataService';

export default function Partidos() {
    const { data, isLoading, error } = useQuery({
        queryKey: ['partidos'],
        queryFn: partidoService.getAll,
    });

    if (isLoading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="text-center">Cargando partidos...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                    Error al cargar partidos: {error.message}
                </div>
            </div>
        );
    }

    const partidos = data?.results || data || [];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-4xl font-bold text-gray-800">Partidos</h1>
            </div>

            {partidos.length === 0 ? (
                <div className="bg-gray-100 p-8 rounded-lg text-center">
                    <p className="text-gray-600">No hay partidos programados</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-4">
                    {partidos.map((partido) => (
                        <div
                            key={partido.id}
                            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition"
                        >
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <h3 className="text-lg font-semibold text-gray-800">
                                        {partido.torneo_nombre || 'Torneo'}
                                    </h3>
                                    <p className="text-sm text-gray-500">
                                        {partido.cancha_nombre || 'Cancha'}
                                    </p>
                                </div>
                                <span className={`px-3 py-1 rounded-full text-sm ${partido.estado === 'finalizado'
                                        ? 'bg-gray-100 text-gray-800'
                                        : partido.estado === 'en_curso'
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-blue-100 text-blue-800'
                                    }`}>
                                    {partido.estado}
                                </span>
                            </div>

                            <div className="flex justify-between items-center">
                                <div className="text-sm text-gray-600">
                                    {new Date(partido.fecha).toLocaleDateString()} - {partido.hora}
                                </div>
                                {partido.resultado && (
                                    <div className="text-lg font-bold text-primary-600">
                                        {partido.resultado}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
