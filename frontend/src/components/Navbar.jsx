import { Link } from 'react-router-dom';
import { useState } from 'react';
import { authService } from '../services/authService';

export default function Navbar({ user }) {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const handleLogout = () => {
        authService.logout();
        window.location.href = '/';
    };

    return (
        <nav className="bg-primary-600 text-white shadow-lg">
            <div className="container mx-auto px-4 py-3">
                <div className="flex justify-between items-center">
                    <Link to="/" className="text-xl sm:text-2xl font-bold hover:text-primary-100">
                        ASOPADEL
                    </Link>

                    {/* Desktop Menu */}
                    <div className="hidden md:flex gap-4 lg:gap-6 items-center">
                        {user && (
                            <>
                                <Link to="/dashboard" className="hover:text-primary-200 transition">
                                    Dashboard
                                </Link>
                                <Link to="/torneos" className="hover:text-primary-200 transition">
                                    Torneos
                                </Link>
                                <Link to="/partidos" className="hover:text-primary-200 transition">
                                    Partidos
                                </Link>
                                <Link to="/canchas" className="hover:text-primary-200 transition">
                                    Canchas
                                </Link>
                                {user.es_admin_aso && (
                                    <Link to="/usuarios" className="hover:text-primary-200 transition">
                                        Usuarios
                                    </Link>
                                )}
                            </>
                        )}

                        {user ? (
                            <>
                                <span className="text-primary-100 text-sm lg:text-base">
                                    {user.first_name || user.cedula}
                                </span>
                                <button
                                    onClick={handleLogout}
                                    className="bg-white text-primary-600 px-3 py-1.5 lg:px-4 lg:py-2 rounded hover:bg-primary-50 transition text-sm lg:text-base"
                                >
                                    Salir
                                </button>
                            </>
                        ) : (
                            <>
                                <Link
                                    to="/login"
                                    className="hover:text-primary-200 transition"
                                >
                                    Iniciar Sesión
                                </Link>
                                <Link
                                    to="/register"
                                    className="bg-white text-primary-600 px-3 py-1.5 lg:px-4 lg:py-2 rounded hover:bg-primary-50 transition text-sm lg:text-base"
                                >
                                    Registrarse
                                </Link>
                            </>
                        )}
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="md:hidden text-white focus:outline-none"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            {mobileMenuOpen ? (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            ) : (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            )}
                        </svg>
                    </button>
                </div>

                {/* Mobile Menu */}
                {mobileMenuOpen && (
                    <div className="md:hidden mt-4 pb-4 space-y-2">
                        {user ? (
                            <>
                                <Link to="/dashboard" className="block py-2 hover:text-primary-200 transition">
                                    Dashboard
                                </Link>
                                <Link to="/torneos" className="block py-2 hover:text-primary-200 transition">
                                    Torneos
                                </Link>
                                <Link to="/partidos" className="block py-2 hover:text-primary-200 transition">
                                    Partidos
                                </Link>
                                <Link to="/canchas" className="block py-2 hover:text-primary-200 transition">
                                    Canchas
                                </Link>
                                {user.es_admin_aso && (
                                    <Link to="/usuarios" className="block py-2 hover:text-primary-200 transition">
                                        Usuarios
                                    </Link>
                                )}
                                <div className="pt-2 border-t border-primary-500">
                                    <p className="text-primary-100 py-2">{user.first_name || user.cedula}</p>
                                    <button
                                        onClick={handleLogout}
                                        className="w-full bg-white text-primary-600 px-4 py-2 rounded hover:bg-primary-50 transition"
                                    >
                                        Salir
                                    </button>
                                </div>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="block py-2 hover:text-primary-200 transition">
                                    Iniciar Sesión
                                </Link>
                                <Link
                                    to="/register"
                                    className="block bg-white text-primary-600 px-4 py-2 rounded hover:bg-primary-50 transition text-center"
                                >
                                    Registrarse
                                </Link>
                            </>
                        )}
                    </div>
                )}
            </div>
        </nav>
    );
}
