import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Torneos from './pages/Torneos';
import Canchas from './pages/Canchas';
import Usuarios from './pages/Usuarios';
import Partidos from './pages/Partidos';
import { authService } from './services/authService';
import './index.css';

const queryClient = new QueryClient();

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      if (authService.isAuthenticated()) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          authService.logout();
        }
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Cargando...</div>
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Navbar user={user} />
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Routes */}
            <Route
              path="/dashboard"
              element={
                authService.isAuthenticated() ? (
                  <Dashboard />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/torneos"
              element={
                authService.isAuthenticated() ? (
                  <Torneos />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/canchas"
              element={
                authService.isAuthenticated() ? (
                  <Canchas />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/usuarios"
              element={
                authService.isAuthenticated() ? (
                  <Usuarios />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/partidos"
              element={
                authService.isAuthenticated() ? (
                  <Partidos />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
