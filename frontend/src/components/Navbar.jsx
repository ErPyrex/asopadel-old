import { Link } from 'react-router-dom';
import { authService } from '../services/authService';

export default function Navbar({ user }) {
    const handleLogout = () => {
        authService.logout();
        window.location.href = '/login';
    };

    return (
        <nav className="bg-primary-600 text-white shadow-lg">
            <div className="container mx-auto px-4 py-3">
                <div className="flex justify-between items-center">
                    <Link to="/" className="text-2xl font-bold hover:text-primary-100">
                        ASOPADEL
                    </Link>

                    <div className="flex gap-6 items-center">
                        <Link to="/torneos" className="hover:text-primary-200 transition">
                            Torneos
                        </Link>
                        <Link to="/partidos" className="hover:text-primary-200 transition">
                            Partidos
                        </Link>
                        <Link to="/canchas" className="hover:text-primary-200 transition">
                            Canchas
                        </Link>
                        {user?.es_admin_aso && (
                            <Link to="/usuarios" className="hover:text-primary-200 transition">
                                Usuarios
                            </Link>
                        )}

                        {user ? (
                            <>
                                <span className="text-primary-100">
                                    {user.first_name || user.cedula}
                                </span>
                                <button
                                    onClick={handleLogout}
                                    className="bg-white text-primary-600 px-4 py-2 rounded hover:bg-primary-50 transition"
                                >
                                    Salir
                                </button>
                            </>
                        ) : (
                            <Link
                                to="/login"
                                className="bg-white text-primary-600 px-4 py-2 rounded hover:bg-primary-50 transition"
                            >
                                Iniciar Sesión
                            </Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}
